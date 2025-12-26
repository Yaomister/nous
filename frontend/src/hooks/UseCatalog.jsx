import { useEffect, useState } from "react";
import { api } from "../axios";

export const UseCatalog = () => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState();
  const [error, setError] = useState();

  useEffect(() => {
    const getData = async () => {
      try {
        const { data: recommended } = await api.get(`/explore/recommend`);
        const { data: popular } = await api.get("/explore/popular");
        const { data: trending } = await api.get("/explore/trending");

        if (recommended && popular) {
          setData({ recommended, popular, trending });
          setLoading(false);
        }
      } catch (e) {
        setError("Cannot load explore page");
      }
    };

    getData();
  }, []);

  return { loading, data, error };
};
