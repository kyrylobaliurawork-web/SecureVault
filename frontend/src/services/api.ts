const API_URL = (
  import.meta.env.VITE_API_URL || ""
).replace(/\/$/, "");

export class ApiError extends Error {
  public status: number;

  constructor(
    message: string,
    status: number,
  ) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

type ApiOptions = RequestInit & {
  token?: string | null;
};

export async function apiRequest<T>(
  path: string,
  options: ApiOptions = {},
): Promise<T> {
  const { token, headers: customHeaders, ...requestOptions } = options;

  const headers = new Headers(customHeaders);

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_URL}${path}`, {
    ...requestOptions,
    headers,
  });

  if (!response.ok) {
    const body = await response.text();
    let message = body || `HTTP ${response.status}`;

    try {
      const parsed = JSON.parse(body);
      message = parsed.detail || message;
    } catch {
      // Відповідь не є JSON — залишаємо звичайний текст.
    }

    throw new ApiError(message, response.status);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export async function apiDownload(
  path: string,
  token: string,
): Promise<Blob> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new ApiError(
      await response.text() || `HTTP ${response.status}`,
      response.status,
    );
  }

  return response.blob();
}