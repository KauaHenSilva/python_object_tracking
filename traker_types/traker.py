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
        self.video = cv2.VideoCapture(video_path)
        
        if not self.video.isOpened():
            print('Erro: Não foi possível carregar o vídeo')
            raise ValueError('Erro: Não foi possível carregar o vídeo')

        self.frame_width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def create_tracker(self, tracker_type):
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


