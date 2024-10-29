export const submitForm = async (data: { username: string; githubUrl: string }) => {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/submit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
  
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
  
    return await response.json();
  };