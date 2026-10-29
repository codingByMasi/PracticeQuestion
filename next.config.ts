import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Content is read from /content with fs at build time; make sure it is traced.
  outputFileTracingIncludes: { "/**": ["./content/**/*"] },
};

export default nextConfig;
