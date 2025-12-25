import "../stylesheets/LogForm.css";
import { Formik } from "formik";
import { HeartIcon } from "./Icons";
import { StarRating } from "./StarRating";
import { api } from "../axios";
import toast, { Toaster } from "react-hot-toast";
import { verifyLog } from "../helpers/BookHelpers";

export const LogForm = ({ details }) => {
  return (
    <div className="log-form-wrapper">
      <Toaster></Toaster>
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
          onSubmit={async (values) => {
            console.error({
              read_before: values.readBefore,
              would_recommend: values.wouldRecommend,
              book_id: details.book_id,
              review: values.review,
              like: values.like,
              rating: values.rating,
            });
            const errors = verifyLog(values);
            if (errors.length > 0) return toast.error(errors[0]);
            try {
              const { status } = await api.post("/book/post", {
                read_before: values.readBefore,
                would_recommend: values.wouldRecommend,
                book_id: details.book_id,
                review: values.review,
                like: values.like,
                rating: values.rating,
              });

              if (status == 200) {
                toast.success("Successfully logged review!");
              } else {
                toast.error("Could not log review");
              }
            } catch (err) {
              toast.error("Could not log review");
            }
          }}
        >
          {(formik) => {
            return (
              <form className="log-form" onSubmit={formik.handleSubmit}>
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
                      action={(rating) => {
                        formik.setFieldValue("rating", rating);
                      }}
                    />
                  </div>

                  <div className="like-button-field-wrapper">
                    <p>Like</p>
                    <button
                      type="button"
                      className={`like-button ${
                        formik.values.like ? "liked" : ""
                      }`}
                      onClick={() => {
                        formik.setFieldValue("like", !formik.values.like);
                      }}
                    >
                      <HeartIcon />
                    </button>
                  </div>
                </div>
                <div className="save-button-wrapper">
                  <button type="submit">Save</button>
                </div>
              </form>
            );
          }}
        </Formik>
      </div>
    </div>
  );
};
