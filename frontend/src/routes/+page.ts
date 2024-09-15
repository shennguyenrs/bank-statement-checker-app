export async function load() {
  const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/v1/statements`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${import.meta.env.VITE_API_TOKEN}`
    }
  });
  const data = await res.json();

  if (data?.rows?.length > 0) {
    return { data };
  }

  return {
    data: {
      rows: []
    }
  };
}
