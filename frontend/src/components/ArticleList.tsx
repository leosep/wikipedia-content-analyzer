import React from 'react';
import { WikipediaSearchArticle } from '../types/wikipedia';
import ArticleCard from './ArticleCard';

interface ArticleListProps {
  articles: WikipediaSearchArticle[];
  onSelectArticle: (article: WikipediaSearchArticle) => void;
}

const ArticleList: React.FC<ArticleListProps> = ({ articles, onSelectArticle }) => {
  return (
    <div className="article-list">
      {articles.length === 0 ? (
        <p>No se encontraron artículos. Prueba con otra búsqueda.</p>
      ) : (
        articles.map((article) => (
          <ArticleCard key={article.pageid} article={article} onSelect={onSelectArticle} />
        ))
      )}
    </div>
  );
};

export default ArticleList;