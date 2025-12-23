import { useState } from "react";
import { useParams } from "react-router-dom";

import "../stylesheets/BookDetails.css";
import { BookmarkIcon, EyeIcon, HeartIcon } from "../components/Icons";
import { Modal } from "../components/Modal";
import { LogForm } from "../components/LogForm";
import { Histogram } from "../components/Histogram";
import { api } from "../axios";
import { useBookDetails } from "../hooks/UseBookDetails";

export const BookDetails = () => {
  const { id } = useParams();
  const [showDetailsPage, setShowDetailsPage] = useState(true);
  const [showLogForm, setShowLogForm] = useState(false);

  const { data, loading, error } = useBookDetails(id);

  if (loading) return <div className="loading-text">Loading details</div>;

  console.error(data);

  return (
    <div className="book-details-page-wrapper">
      {showLogForm && (
        <Modal
          isOpen={showLogForm}
          close={() => setShowLogForm(false)}
          title={"Add a review"}
        >
          <LogForm
            details={{ cover: data.cover, title: data.title, rating: 0 }}
          />
        </Modal>
      )}
      <div className="book-details-top-half">
        <div className="book-details-progress-wrapper">
          <h4 className="title">{data.title}</h4>
          <p className="author">{data.authors[0]}</p>
          <div className="progress-buttons-wrapper">
            <div className="progress-button-field">
              <button>
                <HeartIcon />
              </button>
              <p>Like</p>
            </div>
            <div className="progress-button-field">
              <button>
                <BookmarkIcon />
              </button>
              <p>Save to List</p>
            </div>
            <div className="progress-button-field">
              <button onClick={() => setShowLogForm(true)}>
                <EyeIcon />
              </button>
              <p>Review</p>
            </div>
          </div>
        </div>
        <div className="book-details-cover-wrapper">
          <img
            className="book-cover"
            src={data.cover ? data.cover : "/images/white.png"}
          />
        </div>
      </div>
      <div className="book-details-bottom-half">
        {showDetailsPage ? (
          <div className="book-description-wrapper">
            <h3 className="description-title">Description</h3>
            <p className="description">
              {data.description || "No description avaliable"}
            </p>

            <div className="details-wrapper">
              <h3 className="details-title">Details</h3>
              <div className="details-field">
                <h4>Pages</h4>
                <p>{data.pages || "N/A"}</p>
              </div>
              <div className="details-field">
                <h4>Released</h4>
                <p>{data.release_date || "N/A"}</p>
              </div>
              <div className="details-field">
                <h4>Language</h4>
                <p>{data.language.toUpperCase() || "N/A"}</p>
              </div>
              <div className="details-field">
                <h4>ISBN</h4>
                <p>{data.isbn || "N/A"}</p>
              </div>
            </div>
          </div>
        ) : (
          <div className="book-reviews-wrapper"></div>
        )}

        <div className="book-ratings-wrapper">
          <div className="book-ratings-top-bar">
            <h3 className="book-ratings-title">Book ratings</h3>
            <p>283</p>
          </div>
          <Histogram
            ratings={[3, 4, 2.5, 1, 1.5, 5, 4, 4, 4]}
            averageRating={3}
          />
        </div>
      </div>
    </div>
  );
};

// 3099025a-fea9-463f-86dd-c6509002fb16
