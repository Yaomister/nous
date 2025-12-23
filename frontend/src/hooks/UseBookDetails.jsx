import { useEffect, useState } from "react";
import { api } from "../axios";

export const useBookDetails = (id) => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState();
  const [error, setError] = useState();

  useEffect(() => {
    const getData = async () => {
      setLoading(true);
      setError(null);
      try {
        const { data: _data } = await api.get(`/book/details/${id}`);
        if (_data) {
          setData(_data);
          setLoading(false);
        }
      } catch (e) {
        setError("Cannot load book details");
      }
    };
    getData();
  }, [id]);

  return { loading, data, error };
};
