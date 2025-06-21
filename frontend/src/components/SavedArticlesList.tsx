import React, { useState } from 'react';
import { ArticleInDB } from '../types/article';
import { updateArticleNotes, deleteArticle } from '../api/articles';
import LoadingSpinner from './LoadingSpinner';

interface SavedArticlesListProps {
  articles: ArticleInDB[];
  onArticleDeleted: (id: number) => void;
  onArticleUpdated: (updatedArticle: ArticleInDB) => void;
  isLoading: boolean;
  error: string | null;
  onLoadMore: () => void;
  hasMore: boolean;
}

const SavedArticlesList: React.FC<SavedArticlesListProps> = ({
  articles,
  onArticleDeleted,
  onArticleUpdated,
  isLoading,
  error,
  onLoadMore,
  hasMore,
}) => {
  const [editingArticleId, setEditingArticleId] = useState<number | null>(null);
  const [currentNotes, setCurrentNotes] = useState<string>('');
  const [isUpdating, setIsUpdating] = useState<boolean>(false);
  const [updateError, setUpdateError] = useState<string | null>(null);

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Estás seguro de que deseas eliminar este artículo?')) {
      try {
        await deleteArticle(id);
        onArticleDeleted(id);
      } catch (err) {
        alert('No se pudo eliminar el artículo.');
        console.error(err);
      }
    }
  };

  const handleEditNotes = (article: ArticleInDB) => {
    setEditingArticleId(article.id);
    setCurrentNotes(article.personal_notes || '');
    setUpdateError(null);
  };

  const handleSaveNotes = async (articleId: number) => {
    setIsUpdating(true);
    setUpdateError(null);
    try {
      const updatedArticle = await updateArticleNotes(articleId, currentNotes);
      onArticleUpdated(updatedArticle);
      setEditingArticleId(null);
    } catch (err) {
      console.error('No se pudieron actualizar las notas:', err);
      setUpdateError('No se pudieron actualizar las notas.');
    } finally {
      setIsUpdating(false);
    }
  };

  if (isLoading && articles.length === 0) {
    return <LoadingSpinner />;
  }

  if (error) {
    return <p className="error-message">Error: {error}</p>;
  }

  return (
    <div className="saved-articles-list">
      {articles.length === 0 ? (
        <p>No hay artículos guardados.</p>
      ) : (
        articles.map((article) => (
          <div key={article.id} className="saved-article-item">
            <h3>{article.wikipedia_title}</h3>
            <p>
              <a href={article.wikipedia_url} target="_blank" rel="noopener noreferrer">
                Artículo original
              </a>
            </p>
            <p>Guardado en: {new Date(article.saved_at).toLocaleDateString()}</p>
            <p>Resumen: {article.processed_summary.substring(0, 150)}...</p>
            <p>Cantidad de palabras: {article.word_count}</p>
            <p>
              Palabras frecuentes: {
                Array.isArray(article.frequent_words) && article.frequent_words.length > 0
                  ? article.frequent_words.map(([word, count]) => `${word} (${count})`).join(', ')
                  : 'No se analizaron palabras frecuentes.'
              }
            </p>

            <h3>Análisis de sentimientos:</h3>
      <p>
        <strong>Polaridad:</strong> {article.sentiment_polarity.toFixed(2)}{' '}
        (Varía desde -1.00 para negativo hasta 1.00 para positivo)
      </p>
      <p>
        <strong>Subjetividad:</strong> {article.sentiment_subjectivity.toFixed(2)}{' '}
        (Varía de 0.00 para objetivo a 1.00 para subjetivo)
      </p>
      <p>
        <strong>Sentimiento general:</strong>{' '}
        <span
          style={{
            fontWeight: 'bold',
            color:
              article.sentiment_label === 'positivo'
                ? 'green'
                : article.sentiment_label === 'negativo'
                ? 'red'
                : 'gray',
          }}
        >
          {article.sentiment_label.charAt(0).toUpperCase() + article.sentiment_label.slice(1)}
        </span>
      </p>

            <div className="notes-section">
              {editingArticleId === article.id ? (
                <>
                  <textarea
                    value={currentNotes}
                    onChange={(e) => setCurrentNotes(e.target.value)}
                    rows={4}
                    placeholder="Introduce tus notas..."
                  ></textarea>
                  <button onClick={() => handleSaveNotes(article.id)} disabled={isUpdating}>
                    {isUpdating ? 'Guardando...' : 'Guardar notas'}
                  </button>
                  <button onClick={() => setEditingArticleId(null)} disabled={isUpdating}>
                    Cancelar
                  </button>
                  {updateError && <p className="error-message">{updateError}</p>}
                </>
              ) : (
                <>
                  <p>
                    **Notas personales:** {article.personal_notes || 'Aún no hay notas.'}
                  </p>
                  <button onClick={() => handleEditNotes(article)}>Editar notas</button>
                </>
              )}
            </div>
            <button onClick={() => handleDelete(article.id)} className="delete-button">
              Eliminar
            </button>
          </div>
        ))
      )}
      {hasMore && (
        <button onClick={onLoadMore} disabled={isLoading}>
          {isLoading ? 'Cargando más...' : 'Cargar más'}
        </button>
      )}
    </div>
  );
};

export default SavedArticlesList;