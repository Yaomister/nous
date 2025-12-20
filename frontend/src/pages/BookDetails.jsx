import { useState } from "react";
import { useParams } from "react-router-dom";

import "../stylesheets/BookDetails.css";
import { BookmarkIcon, EyeIcon, HeartIcon } from "../components/Icons";
import { Modal } from "../components/Modal";
import { LogForm } from "../components/LogForm";
import { Histogram } from "../components/Histogram";

export const BookDetails = () => {
  const { id } = useParams();
  const [showDetailsPage, setShowDetailsPage] = useState(true);
  const [showLogForm, setShowLogForm] = useState(false);

  return (
    <div className="book-details-page-wrapper">
      {showLogForm && (
        <Modal
          isOpen={showLogForm}
          close={() => setShowLogForm(false)}
          title={"Add a review"}
        >
          <LogForm />
        </Modal>
      )}
      <div className="book-details-top-half">
        <div className="book-details-progress-wrapper">
          <h4 className="title">Title</h4>
          <p className="author">by john doe</p>
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
            src="https://m.media-amazon.com/images/I/811iBn28JdL._AC_UF894,1000_QL80_.jpg"
          />
        </div>
      </div>
      <div className="book-details-bottom-half">
        {showDetailsPage ? (
          <div className="book-description-wrapper">
            <h3 className="description-title">Description</h3>
            <p className="description">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vitae
              sapien sed risus porttitor tempus. Sed aliquet purus quis metus
              mattis, nec malesuada lacus rhoncus. Lorem ipsum dolor sit amet,
              consectetur adipiscing elit. Praesent iaculis, augue vulputate
              lobortis finibus, urna ante finibus felis, eu dapibus ipsum nibh a
              odio. Proin eget neque lacinia, volutpat est quis, convallis
              augue. Duis sed porttitor justo. Aliquam vel elementum neque, ac
              convallis orci. Maecenas mollis nisl at egestas tincidunt. Proin
              eget eleifend eros. Phasellus sapien lorem, mollis eget ipsum
              eget, condimentum cursus orci. Nulla vehicula ipsum tellus, vel
              posuere nisi hendrerit at. Nam nec sem nec urna imperdiet
              lobortis. Aenean eu sapien ut purus egestas malesuada. Morbi
              accumsan, quam id suscipit lacinia, mi tellus pellentesque mauris,
              nec congue ipsum mauris eget lectus. Sed ullamcorper imperdiet
              eleifend. Suspendisse velit est, venenatis vitae consequat in,
              iaculis nec nunc. Aenean venenatis nulla tellus, eu finibus enim
              convallis sed. Aenean a viverra ipsum, sed maximus lectus. Nunc
              pretium felis eget ipsum interdum, quis ultricies sem malesuada.
              Vestibulum augue erat, ultrices a facilisis sed, euismod sit amet
              erat. Mauris vitae erat venenatis, volutpat sapien venenatis,
              dictum ligula. Fusce non convallis urna. Ut eget pharetra mauris.
              Nam varius ligula nulla, eget tincidunt justo pellentesque sit
              amet. Morbi ut elit felis. Suspendisse condimentum eu risus
              consequat pharetra. Suspendisse tempus in enim et aliquam. Sed ac
              purus nec elit congue feugiat. Quisque id finibus elit. Vivamus
              rutrum dignissim luctus. Aenean posuere commodo risus, quis
              pretium urna dignissim quis. Donec magna felis, ornare a nibh at,
              mattis dignissim dolor. Curabitur ultrices at metus ut sagittis.
              Cras pellentesque lacinia interdum. Nullam posuere nisl sit amet
              aliquet scelerisque. Cras eleifend pharetra risus volutpat
              tincidunt. Proin eget sodales ligula. Donec felis est, porttitor
              convallis orci a, mattis convallis massa.
            </p>

            <div className="details-wrapper">
              <h3 className="details-title">Details</h3>
              <div className="details-field">
                <h4>Pages</h4>
                <p>100</p>
              </div>
              <div className="details-field">
                <h4>Released</h4>
                <p>September 1st 2025</p>
              </div>
              <div className="details-field">
                <h4>Language</h4>
                <p>English</p>
              </div>
              <div className="details-field">
                <h4>ISBN</h4>
                <p>12312213213</p>
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
