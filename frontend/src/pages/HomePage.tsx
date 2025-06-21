import React, { useState, useCallback } from 'react'; 
import SearchBar from '../components/SearchBar';
import ArticleList from '../components/ArticleList';
import ArticleDetail from '../components/ArticleDetail';
import LoadingSpinner from '../components/LoadingSpinner';
import { WikipediaSearchArticle, WikipediaArticleDetail } from '../types/wikipedia';
import { ArticleCreate } from '../types/article';
import { searchWikipedia, getArticleDetails } from '../api/wikipedia';
import { saveArticle } from '../api/articles';

const HomePage: React.FC = () => {
    const [searchResults, setSearchResults] = useState<WikipediaSearchArticle[]>([]);
    const [selectedArticle, setSelectedArticle] = useState<WikipediaArticleDetail | null>(null);
    const [isLoadingSearch, setIsLoadingSearch] = useState(false);
    const [isLoadingDetail, setIsLoadingDetail] = useState(false);
    const [isSavingArticle, setIsSavingArticle] = useState(false);
    const [searchError, setSearchError] = useState<string | null>(null);
    const [detailError, setDetailError] = useState<string | null>(null);
    const [saveError, setSaveError] = useState<string | null>(null);

    const handleSearch = useCallback(async (query: string) => {
        setSearchResults([]);
        setSelectedArticle(null);
        setIsLoadingSearch(true);
        setSearchError(null);
        try {
            const articles = await searchWikipedia(query, 20);
            setSearchResults(articles);
        } catch (err: any) { 
            setSearchError(err.message || 'Error en la búsqueda en Wikipedia. Inténtalo de nuevo.');
            console.error("Error de búsqueda:", err);
        } finally {
            setIsLoadingSearch(false);
        }
    }, []); 

    const handleSelectArticle = useCallback(async (article: WikipediaSearchArticle) => {
        setSelectedArticle(null);
        setIsLoadingDetail(true);
        setDetailError(null);
        try {
            const detailedArticle = await getArticleDetails(article.title);
            setSelectedArticle(detailedArticle);
        } catch (err: any) {
            setDetailError(err.message || 'No se pudieron obtener los detalles del artículo. Inténtalo de nuevo.');
            console.error("Error de obtención de detalles:", err);
        } finally {
            setIsLoadingDetail(false);
        }
    }, []);

    const handleSaveArticle = useCallback(async (article: ArticleCreate) => {
        setIsSavingArticle(true);
        setSaveError(null);
        try {
            await saveArticle(article);
            alert('¡Artículo guardado exitosamente!');
            setSelectedArticle(null); 
        } catch (err: any) {
            setSaveError(err.message || 'No se pudo guardar el artículo. Inténtalo de nuevo.');
            console.error("Error al guardar artículo:", err);
        } finally {
            setIsSavingArticle(false);
        }
    }, []);

    return (
        <div className="home-page">
            <h1>Analizador de contenido de Wikipedia</h1>
            <SearchBar onSearch={handleSearch} />

            {searchError && <p className="error-message">{searchError}</p>}
            {isLoadingSearch ? (
                <LoadingSpinner />
            ) : (
                !selectedArticle && searchResults.length > 0 && (
                    <ArticleList articles={searchResults} onSelectArticle={handleSelectArticle} />
                )
            )}

            {detailError && <p className="error-message">{detailError}</p>}
            {isLoadingDetail ? (
                <LoadingSpinner />
            ) : (
                selectedArticle && (
                    <ArticleDetail
                        article={selectedArticle}
                        onSave={handleSaveArticle}
                        isSaving={isSavingArticle}
                        saveError={saveError}
                    />
                )
            )}
            {}
            {!isLoadingSearch && !searchError && searchResults.length === 0 && !selectedArticle && (
                <p>¡Comienza buscando un artículo en Wikipedia!</p>
            )}
        </div>
    );
};

export default HomePage;