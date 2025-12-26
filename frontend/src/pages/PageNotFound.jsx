import "../stylesheets/PageNotFound.css";

export const PageNotFound = () => {
  return (
    <div className="page-not-found-wrapper">
      <div className="page-not-found">
        <img
          className="page-not-found-gif"
          src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExamFhd2I2OXl2c2Mzc2x2dHJiN3NldGM2NjJwcjNmY3FpaWk4YXFxNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/55SfA4BxofRBe/giphy.gif"
        />
        <div className="page-not-found-message">
          <h1>404</h1>
          <h2>Why are you here?</h2>
          <a href="/">Back to home page</a>
        </div>
      </div>
    </div>
  );
};
