from traker import ObjectTracker
import cv2
import argparse
import sys

class SingleTracker(ObjectTracker):
    def __init__(self, tracker_type, video_path):
        super().__init__(tracker_type, video_path)



    def process_video(self, initial_bbox, output_path=None, single_frame=False):
        """
        Executa o processamento completo do vídeo.
        
        Args:
            initial_bbox (tuple): Região de interesse inicial (x, y, largura, altura)
            output_path (str): Caminho para salvar o vídeo processado
            single_frame (bool): Processar apenas um frame para testes
        """
        # Inicialização do rastreador
        success, frame = self.video.read()
        if not success:
            print('[Erro]: Não foi possível ler o primeiro frame')
            sys.exit()
        
        if not initial_bbox:
            initial_bbox = cv2.selectROI('Selecione a região de interesse', frame, fromCenter=False)
            print('[LOG] Região de interesse selecionada:', initial_bbox)
            cv2.destroyAllWindows()
        
        x, y, w, h = initial_bbox
        if x < 0 or y < 0 or w <= 0 or h <= 0 or (x + w) > frame.shape[1] or (y + h) > frame.shape[0]:
            print("[Erro]: Bounding box inválida ou fora dos limites do frame")
            sys.exit()

        if not self.tracker.init(frame, (x, y, w, h)):
            print('[Erro]: Falha na inicialização do rastreador')
            sys.exit()

        # Configuração do output de vídeo
        output_path = output_path or 'output.avi'
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_writer = cv2.VideoWriter(
            output_path, 
            fourcc, 
            20.0, 
            (self.frame_width, self.frame_height)
        )

        print('[LOG] Processando vídeo...')

        # Loop principal de processamento
        while True:
            success, frame = self.video.read()
            if not success:
                break

            processed_frame, tracking_success, _ = self.process_frame(frame)
            video_writer.write(processed_frame)

            if single_frame:
                break

        # Limpeza de recursos
        self.video.release()
        video_writer.release()
        try:
          cv2.destroyAllWindows()
        except:
          pass
        print('[LOG] Processamento concluído com sucesso')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Sistema de rastreamento de objetos em vídeos usando OpenCV',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        '--tracker_type', 
        required=True,
        choices=['BOOSTING', "MIL", "KCF", "TLD", "MEDIANFLOW", "MOSSE", "CSRT"],
        help='Tipo de algoritmo de rastreamento'
    )
    
    parser.add_argument(
        '--video', 
        required=True,
        help='Caminho para o arquivo de vídeo de entrada'
    )
    
    parser.add_argument(
        '--start_roi', 
        nargs=4, 
        type=int,
        metavar=('X', 'Y', 'LARGURA', 'ALTURA'),
        help='Coordenadas iniciais da região de interesse'
    )
    
    parser.add_argument(
        '--output', 
        help='Caminho para o arquivo de vídeo de saída'
    )
    
    parser.add_argument(
        '--single-frame', 
        action='store_true',
        help='Processar apenas um frame para testes rápidos'
    )

    args = parser.parse_args()

    # Execução do programa
    tracker = ObjectTracker(
        tracker_type=args.tracker_type,
        video_path=args.video
    )
    
    tracker.process_video(
        initial_bbox=args.start_roi,
        output_path=args.output,
        single_frame=args.single_frame
    )