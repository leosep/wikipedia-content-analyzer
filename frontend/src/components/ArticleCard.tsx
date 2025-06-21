import React from 'react';
import { WikipediaSearchArticle } from '../types/wikipedia';

interface ArticleCardProps {
  article: WikipediaSearchArticle;
  onSelect: (article: WikipediaSearchArticle) => void;
}

const ArticleCard: React.FC<ArticleCardProps> = ({ article, onSelect }) => {
  return (
    <div className="article-card" onClick={() => onSelect(article)}>
      <h3>{article.title}</h3>
      <p>{article.url}</p> { }
    </div>
  );
};

export default ArticleCard;