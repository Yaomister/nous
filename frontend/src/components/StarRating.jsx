import { useState } from "react";

import "../stylesheets/StarRating.css";

export const StarRating = ({ _rating, action, disabled }) => {
  const [rating, setRating] = useState(_rating ?? 0);
  const [hoverRating, setHoverRating] = useState(0);

  const stars = Array(5).fill(0);

  return (
    <div className="star-rating-wrapper">
      {stars.map((_, index) => {
        const displayRating = hoverRating || rating;
        return (
          <svg
            key={index}
            className={`star
              ${index + 1 <= displayRating ? "active" : ""}
              ${index + 0.5 === displayRating ? "half" : ""}
            `}
            onClick={
              !disabled &&
              ((e) => {
                const { left, width } = e.currentTarget.getBoundingClientRect();
                const x = e.clientX - left;
                const value = x < width / 2 ? index + 0.5 : index + 1;
                setRating(value);
                if (action) {
                  action(value);
                }
              })
            }
            onMouseOver={
              !disabled &&
              ((e) => {
                const { left, width } = e.currentTarget.getBoundingClientRect();
                const x = e.clientX - left;
                setHoverRating(x < width / 2 ? index + 0.5 : index + 1);
              })
            }
            onMouseLeave={
              !disabled &&
              (() => {
                setHoverRating(0);
              })
            }
            viewBox="0 0 24 24"
          >
            <path d="M12 .587l3.668 7.568L24 9.748l-6 5.848 1.417 8.266L12 19.896l-7.417 3.966L6 15.596 0 9.748l8.332-1.593z" />
          </svg>
        );
      })}
    </div>
  );
};
