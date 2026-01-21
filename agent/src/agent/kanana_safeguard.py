"""
Kakao Kanana Safeguard Model Integration
"""
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict, Tuple
from functools import lru_cache


class KananaSafeguard:
    """Kakao Kanana Safeguard model wrapper for content moderation"""
    
    # Model repository on Hugging Face
    BASE_MODEL = "kakaobrain/kanana-safeguard"
    SIREN_MODEL = "kakaobrain/kanana-safeguard-siren"
    PROMPT_MODEL = "kakaobrain/kanana-safeguard-prompt"
    
    def __init__(self):
        """Initialize Kanana Safeguard models (lazy loading)"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._base_model = None
        self._base_tokenizer = None
        self._siren_model = None
        self._siren_tokenizer = None
        self._prompt_model = None
        self._prompt_tokenizer = None
    
    @property
    def base_model(self):
        """Lazy load base safeguard model"""
        if self._base_model is None:
            self._base_tokenizer = AutoTokenizer.from_pretrained(self.BASE_MODEL)
            self._base_model = AutoModelForSequenceClassification.from_pretrained(
                self.BASE_MODEL
            ).to(self.device)
        return self._base_model
    
    @property
    def base_tokenizer(self):
        if self._base_tokenizer is None:
            _ = self.base_model  # Trigger lazy loading
        return self._base_tokenizer
    
    @property
    def siren_model(self):
        """Lazy load siren (legal risk) model"""
        if self._siren_model is None:
            self._siren_tokenizer = AutoTokenizer.from_pretrained(self.SIREN_MODEL)
            self._siren_model = AutoModelForSequenceClassification.from_pretrained(
                self.SIREN_MODEL
            ).to(self.device)
        return self._siren_model
    
    @property
    def siren_tokenizer(self):
        if self._siren_tokenizer is None:
            _ = self.siren_model
        return self._siren_tokenizer
    
    @property
    def prompt_model(self):
        """Lazy load prompt injection detection model"""
        if self._prompt_model is None:
            self._prompt_tokenizer = AutoTokenizer.from_pretrained(self.PROMPT_MODEL)
            self._prompt_model = AutoModelForSequenceClassification.from_pretrained(
                self.PROMPT_MODEL
            ).to(self.device)
        return self._prompt_model
    
    @property
    def prompt_tokenizer(self):
        if self._prompt_tokenizer is None:
            _ = self.prompt_model
        return self._prompt_tokenizer
    
    def check_content_safety(self, text: str, threshold: float = 0.5) -> Tuple[bool, Dict]:
        """
        Check if content is safe (harmful content detection)
        
        Args:
            text: Input text to check
            threshold: Classification threshold (0-1)
        
        Returns:
            (is_safe, scores) - is_safe: True if safe, False if harmful
        """
        inputs = self.base_tokenizer(
            text, 
            return_tensors="pt", 
            truncation=True, 
            max_length=512
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.base_model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)
        
        # Assuming label 0 = safe, label 1 = harmful
        harmful_score = probs[0][1].item()
        is_safe = harmful_score < threshold
        
        return is_safe, {
            "harmful_score": harmful_score,
            "safe_score": probs[0][0].item(),
            "threshold": threshold
        }
    
    def check_legal_risk(self, text: str, threshold: float = 0.5) -> Tuple[bool, Dict]:
        """
        Check for legal risks (privacy, IP rights)
        
        Returns:
            (is_safe, scores)
        """
        inputs = self.siren_tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.siren_model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)
        
        risk_score = probs[0][1].item()
        is_safe = risk_score < threshold
        
        return is_safe, {
            "risk_score": risk_score,
            "safe_score": probs[0][0].item(),
            "threshold": threshold
        }
    
    def check_prompt_injection(self, text: str, threshold: float = 0.5) -> Tuple[bool, Dict]:
        """
        Check for prompt injection attacks
        
        Returns:
            (is_safe, scores)
        """
        inputs = self.prompt_tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.prompt_model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)
        
        attack_score = probs[0][1].item()
        is_safe = attack_score < threshold
        
        return is_safe, {
            "attack_score": attack_score,
            "safe_score": probs[0][0].item(),
            "threshold": threshold
        }
    
    def check_all(self, text: str, threshold: float = 0.5) -> Tuple[bool, Dict]:
        """
        Run all safeguard checks
        
        Returns:
            (is_safe, detailed_results)
        """
        content_safe, content_scores = self.check_content_safety(text, threshold)
        legal_safe, legal_scores = self.check_legal_risk(text, threshold)
        prompt_safe, prompt_scores = self.check_prompt_injection(text, threshold)
        
        is_safe = content_safe and legal_safe and prompt_safe
        
        return is_safe, {
            "is_safe": is_safe,
            "content_safety": content_safe,
            "legal_safety": legal_safe,
            "prompt_safety": prompt_safe,
            "scores": {
                "content": content_scores,
                "legal": legal_scores,
                "prompt": prompt_scores
            }
        }


# Singleton instance
_kanana_safeguard = None


@lru_cache(maxsize=1)
def get_kanana_safeguard() -> KananaSafeguard:
    """Get or create Kanana Safeguard instance"""
    global _kanana_safeguard
    if _kanana_safeguard is None:
        _kanana_safeguard = KananaSafeguard()
    return _kanana_safeguard
