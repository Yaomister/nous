import { StarRating } from "./StarRating";

import "../stylesheets/Histogram.css";

export const Histogram = ({ ratings, averageRating }) => {
  const count = {
    0.5: 0,
    1: 0,
    1.5: 0,
    2: 0,
    2.5: 0,
    3: 0,
    3.5: 0,
    4: 0,
    4.5: 0,
    5: 0,
  };

  ratings.forEach((rating) => {
    count[rating]++;
  });

  return (
    <div className="histogram-wrapper">
      <div className="histogram-bars">
        {Object.entries(count).map(([rating, amount]) => {
          return (
            <div key={rating} className="histogram-bar">
              <div
                className="histogram-bar-fill"
                style={{
                  height: `${
                    (amount / Math.max(...Object.values(count), 1) + 0.01) * 100
                  }%`,
                }}
              />
            </div>
          );
        })}
      </div>
      <div className="five-star-wrapper">
        <h4>{averageRating}</h4>
        <StarRating disabled={true} _rating={averageRating} />
      </div>
    </div>
  );
};
