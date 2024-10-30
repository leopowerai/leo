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
      throw new Error(errorData.message || 'Network response was not ok');
    }
  
    return await response.json();
  };

export const updatePbiStatus = async(data: {  username : string; status: string }) => {
  const response = await fetch(`${import.meta.env.VITE_API_URL}/update_status`, {
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

export const unassign = async(data: {  username : string }) => {
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

export const hasInProgress = async( username : string ) => {
  const response = await fetch(`${import.meta.env.VITE_API_URL}/has_in_progress/${encodeURIComponent(username)}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    }
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || 'Network response was not ok');
  }

  return await response.json();
};