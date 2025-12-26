import { useNavigate, useParams } from "react-router-dom";
import "../stylesheets/Search.css";
import { useSearch } from "../hooks/useSearch";
import { Loading } from "../components/Loading";
import { useState } from "react";

import "../stylesheets/Search.css";

export const Search = () => {
  const { query } = useParams();
  const [page, setPage] = useState(1);
  const navigate = useNavigate();

  const { data, loading } = useSearch(query, page);

  if (loading == true) return <Loading />;

  return (
    <div className="search-page-wrapper">
      <div className="return-button-wrapper">
        <a href="/explore">Return to explore page</a>
      </div>

      <h3 className="search-page-title">{`Showing search results for "${query}"`}</h3>
      <div className="search-results-wrapper">
        <div className="search-results">
          {data.books.length == 0 && (
            <div className="no-results-found">
              <h4>No results found</h4>
            </div>
          )}
          {data.books.map((book) => {
            return (
              <div
                className="search-result-book"
                onClick={() => navigate(`/book/${book.id}`)}
              >
                <div className="cover-wrapper">
                  <img src={book.cover} />
                </div>
                <div className="title-wrapper">
                  <h3>{book.title}</h3>
                  <p>by {book.authors ? book.authors[0] : "unknown"}</p>
                </div>
              </div>
            );
          })}
        </div>
        <div className="pagination">
          <button
            className="change-page-button"
            onClick={() => {
              setPage((prev) => {
                if (prev > 1) return prev - 1;
                return prev;
              });
            }}
          >
            Previous
          </button>

          <p className="current-page">{`Page ${page} of ${data.total_pages}`}</p>
          <button
            className="change-page-button"
            onClick={() => {
              setPage((prev) => {
                if (prev < data.total_pages) {
                  return prev + 1;
                }
                return prev;
              });
            }}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
};
