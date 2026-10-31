// Synthetic, intentionally tiny example for the code-flow-map skill.
export type User = { id: string; email: string };

export async function lookupUser(email: string): Promise<User | null> {
  if (!email) return null;
  return { id: 'demo-1', email };
}

export async function authenticate(email: string): Promise<User | null> {
  return lookupUser(email);
}

export async function postLogin(request: { email: string }) {
  const user = await authenticate(request.email);
  return { status: user ? 200 : 401, user };
}
