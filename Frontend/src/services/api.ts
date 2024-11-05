import axios, { AxiosError } from 'axios';

export class ApiError extends Error {
  statusCode?: number;

  constructor(message: string, statusCode?: number) {
    super(message);
    this.name = 'ApiError';
    this.statusCode = statusCode;
  }
}

// Define the structure of the error response data
interface ErrorResponse {
  error?: string;
}

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    const message =
      (error.response?.data as ErrorResponse)?.error || error.message || 'Network response was not ok';
    return Promise.reject(new ApiError(message, error.response?.status));
  }
);

export const submitForm = async (data: { username: string }) => {
  const response = await apiClient.post('/submit', data);
  return response.data;
};

export const updatePbiStatus = async (data: { pbiId: string; status: string; urlPR?: string }) => {
  const response = await apiClient.post('/update_pbi_status', data);
  return response.data;
};

export const unassign = async (data: { username: string; pbiId: string }) => {
  const response = await apiClient.post('/unassign', data);
  return response.data;
};

export const isAssigned = async (username: string) => {
  const response = await apiClient.post('/is_assigned', username);
  return response.data;
};

export const assign = async (data: { username: string, pbiId: string }) => {
  const response = await apiClient.post('/assign', data);
  return response.data;
};
