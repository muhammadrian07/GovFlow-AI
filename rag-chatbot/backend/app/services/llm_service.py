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
            
            # Create BALANCED system message
            system_message = """You are a government policy assistant specializing in regulations and policies.

RULES:
1. ONLY answer based on the provided context documents
2. Extract and synthesize relevant information from the documents
3. If the context contains information that directly or indirectly answers the question, use it
4. If the context does NOT contain relevant policy/regulation information for the question, respond:
   "I don't have information about that in the available documents."
5. Do NOT provide general knowledge that is not in the context
6. Do NOT answer questions about weather, current events, or non-policy topics

Your responses MUST be grounded in the provided government policy documents ONLY."""
            
            user_message = f"""Government Policy Documents Context:
{context}

User Question: {query}

Provide your response based ONLY on the context above. If context doesn't address the question, say so clearly."""
            
            # Call Groq API
            answer = self._call_groq_api(system_message, user_message)
            
            logger.info(f"Generated answer for query: {query[:50]}...")
            return answer
        
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            raise
    
    def generate_answer_without_context(self, query: str, country: str = None) -> str:
        """
        Generate a general answer using Groq LLM without RAG context.
        Used for policy-related questions when documents aren't available.
        Rejects non-policy questions and validates country filter.
        
        Args:
            query: User's question
            country: Selected country filter (to validate question is about selected country)
            
        Returns:
            Generated answer from Groq LLM
        """
        try:
            # System message - STRICT about policy focus AND country filter
            system_message = f"""You are a government policy assistant.

CONTEXT:
- User has selected FILTER: {country} policies
- Only help with {country} policy and regulation questions

RULES:
1. Only answer {country} policy, regulations, laws, and government administration questions
2. If question mentions OTHER countries or regions, REJECT it with: "You've selected {country} filter. Your question is about [other_country], which is different. Please change the country filter or ask about {country} policies."
3. Reject weather, sports, entertainment, cooking, or non-policy topics
4. Keep responses professional and focused on governance
5. Guide users back to {country} policy-related questions

IMPORTANT: If the question is about a different country than {country}, REJECT it regardless of topic."""
            
            user_message = query
            
            # Call Groq API
            answer = self._call_groq_api(system_message, user_message)
            
            logger.info(f"Generated general answer for query: {query[:50]}... (country filter: {country})")
            return answer
        
        except Exception as e:
            logger.error(f"Error generating general answer: {str(e)}")
            raise
            
            user_message = query
            
            # Call Groq API without context
            answer = self._call_groq_api(system_message, user_message)
            
            logger.info(f"Generated general answer for query: {query[:50]}...")
            return answer
        
        except Exception as e:
            logger.error(f"Error generating general answer: {str(e)}")
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
