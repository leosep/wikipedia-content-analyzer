import React, { useState } from 'react';
import { WikipediaArticleDetail } from '../types/wikipedia';
import { ArticleCreate } from '../types/article';

interface ArticleDetailProps {
  article: WikipediaArticleDetail;
  onSave: (article: ArticleCreate) => void;
  isSaving: boolean;
  saveError: string | null;
}

const ArticleDetail: React.FC<ArticleDetailProps> = ({ article, onSave, isSaving, saveError }) => {
  const [personalNotes, setPersonalNotes] = useState<string>('');

  const handleSave = () => {
    onSave({
      wikipedia_title: article.title,
      wikipedia_url: article.url,
      processed_summary: article.summary,
      word_count: article.word_count,
      frequent_words: article.frequent_words.map(([word, count]) => [word, count]),
      personal_notes: personalNotes || null,
      sentiment_polarity: article.sentiment_polarity,
      sentiment_subjectivity: article.sentiment_subjectivity,
      sentiment_label: article.sentiment_label,
      user_id: 1,
    });
  };

  return (
    <div className="article-detail">
      <h2>{article.title}</h2>
      <a href={article.url} target="_blank" rel="noopener noreferrer">
        Leer el artículo original en Wikipedia
      </a>
      <p>
        <strong>Resumen:</strong> {article.summary}
      </p>
      <p>
        <strong>Cantidad de palabras:</strong> {article.word_count}
      </p>
      <p>
        {}
        <strong>Palabras más frecuentes:</strong> {article.frequent_words.join(', ')} 
      </p>

      {}
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
      {}

      <div className="personal-notes">
        <h3>Notas personales:</h3>
        <textarea
          placeholder="Añade tus notas personales aquí..."
          value={personalNotes}
          onChange={(e) => setPersonalNotes(e.target.value)}
        ></textarea>
      </div>

      <button onClick={handleSave} disabled={isSaving}>
        {isSaving ? 'Guardando...' : 'Guardar artículo'}
      </button>
      {saveError && <p className="error-message">{saveError}</p>}
    </div>
  );
};

export default ArticleDetail;