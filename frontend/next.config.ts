import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  output: 'standalone',
  experimental: {
    serverActions: {
      allowedOrigins: ['localhost:3000', 'localhost:8000']
    }
  }
};

export default nextConfig;
