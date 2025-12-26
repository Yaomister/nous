import { Loading } from "../components/Loading";
import { UseCatalog } from "../hooks/UseCatalog";
import "../stylesheets/Home.css";
import { useNavigate } from "react-router-dom";

const getGreeting = () => {
  const hour = new Date().getHours();
  if (hour >= 5 && hour < 12) return "morning";
  if (hour >= 12 && hour < 17) return "afternoon";
  if (hour >= 17 && hour < 21) return "evening";
  return "night";
};

export const Home = () => {
  const { data, loading } = UseCatalog();
  const navigate = useNavigate();

  if (loading) return <Loading />;

  const { trending } = data;
  return (
    <div className="home-wrapper">
      <div className="trending-books-wrapper">
        <h4 className="greeting-text">{`Good ${getGreeting()}!`}</h4>
        <p>here's what everyone's been reading this week</p>
        <div className="trending-books">
          {trending.map((book) => {
            return (
              <div className="trending-book">
                <img
                  src={book.cover}
                  onClick={() => navigate(`book/${book.id}`)}
                />
              </div>
            );
          })}
        </div>
      </div>
      <div className="stats-wrapper">
        <h4>All time statistics</h4>
        <div className="stats">
          <div className="stat">
            <h1>0</h1>
            <p>Books</p>
          </div>
          <div className="stat">
            <h1>0</h1>
            <p>Authors</p>
          </div>
          <div className="stat">
            <h1>0</h1>
            <p>Pages</p>
          </div>
        </div>
      </div>
    </div>
  );
};
