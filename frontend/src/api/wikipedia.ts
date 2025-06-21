import { WikipediaSearchArticle, WikipediaArticleDetail } from '../types/wikipedia';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const searchWikipedia = async (query: string, limit: number = 20): Promise<WikipediaSearchArticle[]> => {
  
    const response = await fetch(`${API_BASE_URL}/wikipedia/search?query=${encodeURIComponent(query)}&limit=${limit}`);
    if (!response.ok) {

        let errorMessage = `Error al buscar en Wikipedia: ${response.statusText}`;
        try {
            const errorData = await response.json();
            if (errorData && errorData.detail) {
                errorMessage += ` - ${JSON.stringify(errorData.detail)}`;
            }
        } catch (e) {
            console.warn("No se pudo analizar la respuesta de error JSON:", e);
        }
        throw new Error(errorMessage);
    }
    return response.json();
};

export const getArticleDetails = async (title: string): Promise<WikipediaArticleDetail> => {
    const response = await fetch(`${API_BASE_URL}/wikipedia/article/${encodeURIComponent(title)}`);
    if (!response.ok) {
        let errorMessage = `Error al obtener los detalles del artículo: ${response.statusText}`;
        try {
            const errorData = await response.json();
            if (errorData && errorData.detail) {
                errorMessage += ` - ${JSON.stringify(errorData.detail)}`;
            }
        } catch (e) {
            console.warn("No se pudo analizar la respuesta de error JSON:", e);
        }
        throw new Error(errorMessage);
    }
    return response.json();
};