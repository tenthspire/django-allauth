import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000', 
  headers: {
    Authorization: `Bearer ${localStorage.getItem('authToken')}`,
  },
});

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response.status === 401) {
      try {
        const refreshToken = localStorage.getItem('refreshToken');
        const response = await axios.post('http://localhost:8000/api/token/refresh/', {
          refresh: refreshToken,
        });
        localStorage.setItem('authToken', response.data.access);
        error.config.headers.Authorization = `Bearer ${response.data.access}`;
        return axios(error.config);
      } catch (err) {
        console.error('Token refresh failed:', err);
        localStorage.clear();
        window.location.href = '/login'; 
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
