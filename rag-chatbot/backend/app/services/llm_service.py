"""
Language Model service.
Handles interaction with Groq API for LLM generation.
"""

from typing import List, Dict, Any
import httpx
import json
import logging

logger = logging.getLogger(__name__)


class LLMService:
    """
    Service for interacting with Groq Language Models.
    Handles prompt construction and LLM queries using Groq API.
    """
    
    def __init__(self, api_key: str, model: str = "llama-3.1-8b-instant"):
        """
        Initialize Groq LLM service.
        
        Args:
            api_key: Groq API key
            model: Model name to use (default: mixtral-8x7b-32768)
        """
        self.model = model
        self.api_key = api_key
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.temperature = 0.7
        logger.info(f"Groq LLM service initialized with model: {model}")
    
    def generate_answer(
        self,
        query: str,
        context_chunks: List[str]
    ) -> str:
        """
        Generate an answer using context from RAG pipeline via Groq API.
        
        Args:
            query: User's original query
            context_chunks: Retrieved context from vector database
            
        Returns:
            Generated answer from Groq LLM
        """
        try:
            # Construct context string
            context = "\n\n".join(context_chunks)
            
            # Create system and user messages
            system_message = """You are a helpful government policy assistant. 
Answer ONLY using the provided context. If the answer is not in the context, say "I don't have enough information to answer this question.\""""
            
            user_message = f"""Context:
{context}

Question: {query}

Answer:"""
            
            # Call Groq API
            answer = self._call_groq_api(system_message, user_message)
            
            logger.info(f"Generated answer for query: {query[:50]}...")
            return answer
        
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            raise
    
    def _call_groq_api(self, system_message: str, user_message: str) -> str:
        """
        Call Groq API to generate response.
        
        Args:
            system_message: System prompt/instructions
            user_message: User query with context
            
        Returns:
            Generated response from Groq
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                "temperature": self.temperature,
                "max_tokens": 1024
            }
            
            # Make synchronous HTTP call
            with httpx.Client(timeout=60.0) as client:
                response = client.post(self.api_url, json=payload, headers=headers)
                response.raise_for_status()
                
                result = response.json()
                answer = result["choices"][0]["message"]["content"]
                
                logger.info("Groq API call successful")
                return answer
        
        except httpx.HTTPError as e:
            logger.error(f"Groq API HTTP error: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing Groq response: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error calling Groq API: {str(e)}")
            raise
    
    def extract_sources(
        self,
        documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Extract and format sources from retrieved documents.
        
        Args:
            documents: List of retrieved documents
            
        Returns:
            Formatted list of sources
        """
        sources = []
        for doc in documents:
            source = {
                "text": doc.get("text", "")[:200],  # Truncate to 200 chars
                "source": doc.get("source", "Unknown"),
                "page": doc.get("page")
            }
            sources.append(source)
        
        return sources
