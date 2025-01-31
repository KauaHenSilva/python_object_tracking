import cv2
import argparse
import sys


class ObjectTracker:
    """Classe principal para rastreamento de objetos em vídeos usando OpenCV."""

    def __init__(self, tracker_type, video_path):
        """
        Inicializa o rastreador com configurações básicas.
        
        Args:
            tracker_type (str): Tipo de algoritmo de rastreamento
            video_path (str): Caminho para o arquivo de vídeo
        """
        self.tracker_type = tracker_type
        self.tracker = self._create_tracker(tracker_type)
        self.video = cv2.VideoCapture(video_path)
        
        # Verifica se o vídeo foi aberto corretamente
        if not self.video.isOpened():
            print('Erro: Não foi possível carregar o vídeo')
            sys.exit()

        # Obtém propriedades do vídeo
        self.frame_width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def _create_tracker(self, tracker_type):
        """Cria o objeto rastreador com base no tipo especificado."""
        tracker = None
        tracker_types = {
            "BOOSTING": cv2.legacy.TrackerBoosting_create,
            # "MIL": cv2.legacy.TrackerMIL_create,
            # "KCF": cv2.TrackerKCF_create,
            # "TLD": cv2.legacy.TrackerTLD_create,
            # "MEDIANFLOW": cv2.legacy.TrackerMedianFlow_create,
            # "MOSSE": cv2.legacy.TrackerMOSSE_create,
            # "CSRT": cv2.legacy.TrackerCSRT_create
        }

        if tracker_type in tracker_types:
            tracker = tracker_types[tracker_type]()
            print(f"[INFO] Rastreador {tracker_type} selecionado")
        else:
            raise ValueError(f"Tipo de rastreador inválido: {tracker_type}")

        return tracker

    def _process_frame(self, frame):
        """
        Processa um único frame aplicando o algoritmo de rastreamento.
        
        Retorna:
            tuple: (frame processado, status do rastreamento, caixa delimitadora)
        """
        # Medição de performance
        timer_start = cv2.getTickCount()
        success, bbox = self.tracker.update(frame)
        processing_time = (cv2.getTickCount() - timer_start) / cv2.getTickFrequency()

        if success:
            # Desenha a caixa delimitadora
            x, y, w, h = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Adiciona informações overlay
            fps_text = f"FPS: {int(1 / processing_time)}" if processing_time > 0 else "FPS: ∞"
            cv2.putText(frame, self.tracker_type, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, fps_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        return frame, success, bbox

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
            print('Erro: Não foi possível ler o primeiro frame')
            sys.exit()

        if not self.tracker.init(frame, initial_bbox):
            print('Erro: Falha na inicialização do rastreador')
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

        print('[STATUS] Processando vídeo...')

        # Loop principal de processamento
        while True:
            success, frame = self.video.read()
            if not success:
                break

            processed_frame, tracking_success, _ = self._process_frame(frame)
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
        print('[STATUS] Processamento concluído com sucesso')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Sistema de rastreamento de objetos em vídeos usando OpenCV',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        '--tracker_type', 
        required=True,
        choices=['BOOSTING'],
        help='Tipo de algoritmo de rastreamento'
    )
    
    parser.add_argument(
        '--video', 
        required=True,
        help='Caminho para o arquivo de vídeo de entrada'
    )
    
    parser.add_argument(
        '--start_roi', 
        required=True,
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
        initial_bbox=tuple(args.start_roi),
        output_path=args.output,
        single_frame=args.single_frame
    )