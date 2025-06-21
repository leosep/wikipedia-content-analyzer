import { ArticleCreate, ArticleInDB, ArticleUpdate } from '../types/article';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const saveArticle = async (article: ArticleCreate): Promise<ArticleInDB> => {
  const response = await fetch(`${API_BASE_URL}/articles/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(article),
  });

  if (!response.ok) {
    throw new Error(`Error al guardar el artículo: ${response.statusText}`);
  }

  return response.json();
};

export const getSavedArticles = async (skip = 0, limit = 10): Promise<ArticleInDB[]> => {
  const response = await fetch(`${API_BASE_URL}/articles/?skip=${skip}&limit=${limit}`);
  if (!response.ok) {
    throw new Error(`Error al recuperar los artículos guardados: ${response.statusText}`);
  }

  return await response.json();
};

export const updateArticleNotes = async (articleId: number, notes: string | null): Promise<ArticleInDB> => {
  const response = await fetch(`${API_BASE_URL}/articles/${articleId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ personal_notes: notes }),
  });

  if (!response.ok) {
    throw new Error(`Error al actualizar las notas del artículo: ${response.statusText}`);
  }

  return await response.json();
};

export const deleteArticle = async (articleId: number): Promise<void> => {
  const response = await fetch(`${API_BASE_URL}/articles/${articleId}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    throw new Error(`Error al eliminar el artículo: ${response.statusText}`);
  }
};