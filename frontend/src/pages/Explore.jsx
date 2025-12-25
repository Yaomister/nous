import { SearchIcon } from "../components/Icons";
import { UseExplore } from "../hooks/UseExplore";
import { useNavigate } from "react-router-dom";

import "../stylesheets/Explore.css";

export const Explore = () => {
  const { data, loading } = UseExplore();
  const navigate = useNavigate();

  if (loading) return <div>Loading explore page</div>;

  const { recommended, popular } = data;

  return (
    <div className="explore-page-wrapper">
      <div className="search-bar-wrapper">
        <div className="search-bar">
          <SearchIcon />
          <input
            className="bar"
            placeholder="Search for books, authors or paste ISBN"
          ></input>
        </div>
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
