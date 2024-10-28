from PIL import Image
from multilingual_clip import pt_multilingual_clip
import transformers
import open_clip
import torch

from domain import embedder, dto

class CLIPEmbedder(embedder.Embedder):
    def __init__(self):
        self.model = pt_multilingual_clip.MultilingualCLIP.from_pretrained('M-CLIP/XLM-Roberta-Large-Vit-B-16Plus')
        self.tokenizer = transformers.AutoTokenizer.from_pretrained('M-CLIP/XLM-Roberta-Large-Vit-B-16Plus')
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.img_model, _, self.preprocess = open_clip.create_model_and_transforms('ViT-B-16-plus-240',
                                                                                   pretrained="laion400m_e32")
        self.img_model.to(self.device)

    def generate_embedding_text(self, text: str) -> dto.Embedding:
        emb = self.model.forward(text, self.tokenizer)
        return dto.Embedding(data=emb.detach().numpy())

    def generate_embedding_image(self, image_path: str) -> dto.Embedding:
        # TODO: error handling for non-existing file
        image = self.preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)
        with torch.no_grad():
            return dto.Embedding(data=self.img_model.encode_image(image)[0].detach().numpy())