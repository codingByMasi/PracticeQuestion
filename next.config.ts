import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Content is read from /content with fs at build time; make sure it is traced.
  outputFileTracingIncludes: { "/**": ["./content/**/*"] },
  async headers() {
    return [
      // The SQLite binary only changes with the sql.js version.
      { source: "/vendor/:path*", headers: [{ key: "Cache-Control", value: "public, max-age=604800, stale-while-revalidate=86400" }] },
      // The Python worker isn't content-hashed, so always revalidate it.
      { source: "/workers/:path*", headers: [{ key: "Cache-Control", value: "public, max-age=0, must-revalidate" }] },
    ];
  },
};

export default nextConfig;
