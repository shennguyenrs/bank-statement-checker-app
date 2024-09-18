import { API_BASE_URL, API_TOKEN } from '$lib/constants';

export async function load() {
  try {
    const res = await fetch(`${API_BASE_URL}/statements`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${API_TOKEN}`
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
  } catch (error) {
    console.log(error);
    return {
      data: {
        rows: []
      }
    };
  }
}
