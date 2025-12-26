import { SearchIcon } from "../components/Icons";
import { UseCatalog } from "../hooks/UseCatalog";
import { useNavigate } from "react-router-dom";

import "../stylesheets/Explore.css";
import { useState } from "react";
import { Loading } from "../components/Loading";

export const Explore = () => {
  const { data, loading } = UseCatalog();
  const navigate = useNavigate();
  const [query, setQuery] = useState("");

  if (loading) return <Loading />;

  const { recommended, popular } = data;

  return (
    <div className="explore-page-wrapper">
      <div className="search-bar-wrapper">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            navigate(`/search/${query}`);
          }}
        >
          <div className="search-bar">
            <SearchIcon />
            <input
              onChange={(e) => {
                setQuery(e.target.value);
              }}
              className="bar"
              placeholder="Search for books, authors or paste ISBN"
            ></input>
          </div>
        </form>
      </div>
      <div className="recommended-wrapper">
        <h4>Recommended for you</h4>
        <div className="recommended-books-wrapper">
          {recommended.map((book, _) => {
            return (
              <div
                className="explore-book-item"
                onClick={() => navigate(`/book/${book.id}`)}
              >
                <img
                  className="cover"
                  src={book.cover}
                  onError={(e) => {
                    e.currentTarget.onerror = null;
                    e.currentTarget.src = "./images/white.png";
                  }}
                />
                <p4 className="title">{book.title}</p4>
                <p className="author">{`by ${book.authors[0]}`}</p>
              </div>
            );
          })}
        </div>
      </div>
      <div className="most-popular-wrapper">
        <h4>Most popular</h4>
        <div className="most-popular-books-wrapper">
          {popular.map((book, _) => {
            return (
              <div
                className="explore-book-item"
                onClick={() => navigate(`/book/${book.id}`)}
              >
                <img
                  className="cover"
                  src={book.cover}
                  onError={(e) => {
                    e.currentTarget.onerror = null;
                    e.currentTarget.src = "./images/white.png";
                  }}
                />
                <p4 className="title">{book.title}</p4>
                <p className="author">{`by ${book.authors[0]}`}</p>
              </div>
            );
          })}
        </div>
      </div>

      <div className="collections-wrapper">
        <h4>Collections</h4>
        <div className="collections-wrapper"></div>
      </div>
    </div>
  );
};
