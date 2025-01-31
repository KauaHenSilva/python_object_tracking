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
        print(f"[INFO] Carregando vídeo de entrada: {video_path}")
        
        self.tracker_type = tracker_type
        self.tracker = self._create_tracker(tracker_type)
        self.video = cv2.VideoCapture(video_path)
        
        if not self.video.isOpened():
            print('Erro: Não foi possível carregar o vídeo')
            raise ValueError('Erro: Não foi possível carregar o vídeo')

        self.frame_width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def _create_tracker(self, tracker_type):
        """Cria o objeto rastreador com base no tipo especificado."""
        tracker = None
        tracker_types = {
            "BOOSTING": cv2.legacy.TrackerBoosting.create,
            "MIL": cv2.legacy.TrackerMIL.create,
            "KCF": cv2.legacy.TrackerKCF.create,
            "TLD": cv2.legacy.TrackerTLD.create,
            "MEDIANFLOW": cv2.legacy.TrackerMedianFlow.create,
            "MOSSE": cv2.legacy.TrackerMOSSE.create,
            "CSRT": cv2.legacy.TrackerCSRT.create
        }

        if tracker_type in tracker_types:
            tracker = tracker_types[tracker_type]()
            print(f"[INFO] Rastreador {tracker_type} selecionado")
        else:
            raise ValueError(f"Tipo de rastreador inválido: {tracker_type}")

        return tracker

    def process_frame(self, frame):
      """
      Processa um único frame aplicando o algoritmo de rastreamento.
      
      Retorna:
          tuple: (frame processado, status do rastreamento, caixa delimitadora)
      """
      timer_start = cv2.getTickCount()
      success, bbox = self.tracker.update(frame)
      processing_time = (cv2.getTickCount() - timer_start) / cv2.getTickFrequency()

      if success:
          x, y, w, h = [int(v) for v in bbox]
          cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

          fps_text = f"FPS: {int(1 / processing_time)}" if processing_time > 0 else "FPS: NONE"
          cv2.putText(frame, self.tracker_type, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
          cv2.putText(frame, fps_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
      else:
          cv2.putText(frame, "Falha no rastreamento", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

      return frame, success, bbox


