import "../stylesheets/NavBar.css";
import { useAuth } from "../components/AuthContext";

export const NavBar = () => {
  const { user } = useAuth();
  return (
    <div className="nav-bar-wrapper">
      <div className="nav-bar">
        <div className="nav-bar-logo">
          <h1 className="logo">Nous</h1>
        </div>
        <div className="nav-bar-links">
          {user ? (
            <a className="link" href="/profile">
              {user.username}
            </a>
          ) : (
            <>
              <a className="link" href="/login">
                Sign In
              </a>
              <a className="link" href="/register">
                Join
              </a>
            </>
          )}
          <a className="link" href={`/`}>
            Home
          </a>
          <a className="link" href={`/feed`}>
            Feed
          </a>
          <a className="link" href={`/explore`}>
            Explore
          </a>
        </div>
      </div>
    </div>
  );
};
