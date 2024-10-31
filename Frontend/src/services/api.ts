
export class ApiError extends Error {
  statusCode?: number;

  constructor(message: string, statusCode?: number) {
    super(message);
    this.name = 'ApiError';
    this.statusCode = statusCode;
  }
}

export const submitForm = async (data: { username: string; githubUrl: string }) => {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/submit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
  
    if (!response.ok) {
      const errorData = await response.json();
      console.log(errorData.error);
      throw new ApiError(errorData.error || 'Network response was not ok', response.status);
    }
  
    return await response.json();
  };

export const updatePbiStatus = async(data: {  pbiId : string; status: string; urlPR?: string }) => {

  const response = await fetch(`${import.meta.env.VITE_API_URL}/update_pbi_status`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || 'Network response was not ok');
  }

  return await response.json();
};

export const unassign = async(data: {  username : string; pbiId: string }) => {

  const response = await fetch(`${import.meta.env.VITE_API_URL}/unassign`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || 'Network response was not ok');
  }

  return await response.json();
};

export const isAssigned = async (username: string) => {
  const response = await fetch(`${import.meta.env.VITE_API_URL}/is_assigned`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || 'Network response was not ok');
  }

  return await response.json(); // Expected to return { is_assigned: boolean }
};