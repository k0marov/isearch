import logging

from PIL import Image
from multilingual_clip import pt_multilingual_clip
import transformers
import open_clip
import torch

from domain import embedder, dto

class CLIPEmbedder(embedder.Embedder):
    def __init__(self, logger: logging.Logger):
        self._logger = logger
        self._model = pt_multilingual_clip.MultilingualCLIP.from_pretrained('M-CLIP/XLM-Roberta-Large-Vit-B-16Plus')
        self._tokenizer = transformers.AutoTokenizer.from_pretrained('M-CLIP/XLM-Roberta-Large-Vit-B-16Plus')
        self._device = "cuda" if torch.cuda.is_available() else "cpu"
        self._img_model, _, self.preprocess = open_clip.create_model_and_transforms('ViT-B-16-plus-240',
                                                                                    pretrained="laion400m_e32")
        self._img_model.to(self._device)

    def generate_embedding_text(self, text: str) -> dto.Embedding:
        emb = self._model.forward(text, self._tokenizer)
        return dto.Embedding(data=emb.detach().numpy())

    def generate_embedding_image(self, img: Image.Image) -> dto.Embedding:
        image = self.preprocess(img).unsqueeze(0).to(self._device)
        with torch.no_grad():
            return dto.Embedding(data=self._img_model.encode_image(image)[0].detach().numpy())