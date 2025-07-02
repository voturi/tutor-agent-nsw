import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/v1/:path*',
        destination: 'http://localhost:8000/api/v1/:path*',
      },
    ];
  },
  experimental: {
    serverActions: {
      allowedOrigins: ['localhost:3000', 'localhost:8000']
    }
  }
};

export default nextConfig;
