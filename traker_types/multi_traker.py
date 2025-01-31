from traker import ObjectTracker
import cv2
import argparse
import sys
import ast
from random import randint

class SingleTracker(ObjectTracker):
    def __init__(self, tracker_type, video_path):
        super().__init__(tracker_type, video_path)
        self.mult_tracker = cv2.legacy.MultiTracker.create()

    def process_frame(self, frame, colors):
      """
      Processa um único frame aplicando o algoritmo de rastreamento.
      
      Retorna:
          tuple: (frame processado, status do rastreamento, caixa delimitadora)
      """
      timer_start = cv2.getTickCount()
      success, bboxs = self.mult_tracker.update(frame)
      processing_time = (cv2.getTickCount() - timer_start) / cv2.getTickFrequency()

      if success:
          fps_text = f"FPS: {int(1 / processing_time)}" if processing_time > 0 else "FPS: NONE"
          cv2.putText(frame, self.tracker_type, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
          cv2.putText(frame, fps_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
          for bbox, color in zip(bboxs, colors):
            x, y, w, h = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
      else:
          cv2.putText(frame, "Falha no rastreamento", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

      return frame, success

    def process_video(self, initial_bbox, output_path=None, frame_cont=None):
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
            
        bboxs = []
        colors = []
        
        if not initial_bbox:
            while True:
                bboxs.append(cv2.selectROI('Selecione a região de interesse', frame, fromCenter=False))
                colors.append((randint(64, 255), randint(64, 255), randint(64, 255)))
                print("[INFO] Pressione 'q' para finalizar a seleção de ROIs")
                print('[LOG] Região de interesse selecionada:', bboxs[-1])
                if cv2.waitKey(0) & 0xFF == ord('q'):
                    break
        else:
            bboxs = initial_bbox
            colors = [(randint(64, 255), randint(64, 255), randint(64, 255)) for _ in range(len(bboxs))]
        
        print("[INFO] bboxs:", bboxs)
        print("[INFO] colors:", colors)
        
        for bbox in bboxs:
            x, y, w, h = bbox
            if x < 0 or y < 0 or w <= 0 or h <= 0 or (x + w) > frame.shape[1] or (y + h) > frame.shape[0]:
                print("[Erro]: Bounding box inválida ou fora dos limites do frame")
                sys.exit()
            self.mult_tracker.add(self.create_tracker(self.tracker_type), frame, bbox)

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

        while True:
            success, frame = self.video.read()
            if not success:
                break

            processed_frame, tracking_success = self.process_frame(frame, colors)
            video_writer.write(processed_frame)
            
            if frame_cont:
                print("[INFO] Frames restantes:", frame_cont)
                frame_cont -= 1
                if frame_cont <= 0:
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
        type=ast.literal_eval,
        help='Coordenadas iniciais da região de interesse'
    )
    
    parser.add_argument(
        '--output', 
        help='Caminho para o arquivo de vídeo de saída'
    )
    
    parser.add_argument(
        '--frame_cont', 
        type=int,
        help='Número de frames para processar'
    )

    args = parser.parse_args()

    # Execução do programa
    tracker = SingleTracker(
        tracker_type=args.tracker_type,
        video_path=args.video
    )
    
    tracker.process_video(
        initial_bbox=args.start_roi,
        output_path=args.output,
        frame_cont=args.frame_cont
    )