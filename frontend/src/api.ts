export const API_URL = import.meta.env.VITE_API_URL;


export async function graphqlRequest(query: string, variables?: object) {
  const res = await fetch(`${API_URL}/graphql`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(variables ? { query, variables } : { query }),
  });
  return res.json();
}