import React, { useEffect, useState } from 'react';
import SavedArticlesList from '../components/SavedArticlesList';
import { ArticleInDB } from '../types/article';
import { getSavedArticles } from '../api/articles';

const PAGE_SIZE = 10;

const SavedArticlesPage: React.FC = () => {
  const [savedArticles, setSavedArticles] = useState<ArticleInDB[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);

  const fetchSavedArticles = async (page: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const newArticles = await getSavedArticles(page * PAGE_SIZE, PAGE_SIZE);
      setSavedArticles((prevArticles) => {
        const uniqueNewArticles = newArticles.filter(
          (newArt) => !prevArticles.some((prevArt) => prevArt.id === newArt.id)
        );
        return [...prevArticles, ...uniqueNewArticles];
      });
      setHasMore(newArticles.length === PAGE_SIZE);
    } catch (err) {
      setError('No se pudieron recuperar los artículos guardados.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchSavedArticles(currentPage);
  }, [currentPage]);

  const handleArticleDeleted = (id: number) => {
    setCurrentPage(0);
    setSavedArticles((prevArticles) => prevArticles.filter((article) => article.id !== id));
    setCurrentPage(0);
  };

  const handleArticleUpdated = (updatedArticle: ArticleInDB) => {
    setSavedArticles((prevArticles) =>
      prevArticles.map((article) =>
        article.id === updatedArticle.id ? updatedArticle : article
      )
    );
  };

  const handleLoadMore = () => {
    setCurrentPage((prevPage) => prevPage + 1);
  };

  return (
    <div className="saved-articles-page">
      <h1>Mis artículos guardados</h1>
      <SavedArticlesList
        articles={savedArticles}
        onArticleDeleted={handleArticleDeleted}
        onArticleUpdated={handleArticleUpdated}
        isLoading={isLoading}
        error={error}
        onLoadMore={handleLoadMore}
        hasMore={hasMore}
      />
    </div>
  );
};

export default SavedArticlesPage;