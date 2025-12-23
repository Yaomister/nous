import "../stylesheets/LogForm.css";
import { Formik } from "formik";
import { HeartIcon } from "./Icons";
import { StarRating } from "./StarRating";

export const LogForm = ({ details }) => {
  return (
    <div className="log-form-wrapper">
      <div className="log-form-cover-wrapper">
        <img
          className="book-cover"
          src={details.cover ? details.cover : "/images/white.png"}
        />
      </div>
      <div className="log-form-review-wrapper">
        <h4 className="book-title">{details.title}</h4>

        <Formik
          initialValues={{
            readBefore: false,
            wouldRecommend: true,
            review: "",
            rating: 0,
            like: false,
          }}
        >
          {(formik) => {
            return (
              <form className="log-form">
                <div className="checkbox-fields">
                  <div className="checkbox-field">
                    <input
                      type="checkbox"
                      id={"read-before"}
                      onChange={formik.handleChange}
                      value={formik.values.readBefore}
                    />
                    <label form="read-before">I've read this before</label>
                  </div>
                  <div className="checkbox-field">
                    <input
                      type="checkbox"
                      id={"recommend-to-others"}
                      onChange={formik.handleChange}
                      value={formik.values.wouldRecommend}
                    />
                    <label form="recommend-to-others">
                      I would recommend this to others
                    </label>
                  </div>
                </div>
                <textarea
                  placeholder="Add a review..."
                  value={formik.values.review}
                  className="review"
                  onChange={formik.handleChange}
                  name="review"
                />
                <div className="other-ratings">
                  <div className="star-rating-field-wrapper">
                    <p>Rating</p>
                    <StarRating
                      _rating={details.rating ? details._rating : 0}
                    />
                  </div>

                  <div className="like-button-field-wrapper">
                    <p>Like</p>
                    <HeartIcon />
                  </div>
                </div>
              </form>
            );
          }}
        </Formik>
      </div>
    </div>
  );
};
