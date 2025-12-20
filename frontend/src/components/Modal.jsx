import "../stylesheets/Modal.css";
export const Modal = ({ isOpen, close, title, children }) => {
  if (!isOpen) return null;
  return (
    <div className="modal-wrapper" onClick={() => close()}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-top-bar">
          <h4 className="modal-title">{title}</h4>

          <button className="close-button" onClick={() => close()}>
            x
          </button>
        </div>

        <div className="modal-content">{children}</div>
      </div>
    </div>
  );
};
