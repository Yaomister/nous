import { useEffect, useState } from "react";
import { api } from "../axios";

export const useSearch = (query, page) => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState();
  const [error, setError] = useState();

  useEffect(() => {
    console.error(query, page);
    const getData = async () => {
      try {
        const { data: results } = await api.get(
          `/explore/search/${query}/${page}`
        );

        if (results) {
          setData({
            total_pages: results.total_pages,
            books: results.books.filter((book) => book.authors && book.title),
          });
          setLoading(false);
        }
      } catch (e) {
        setError("Cannot load explore page");
      }
    };

    getData();
  }, [query, page]);

  return { loading, data, error };
};
