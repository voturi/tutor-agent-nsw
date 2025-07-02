'use client';

import { useState, useCallback, useEffect } from 'react';
import dynamic from 'next/dynamic';
import { ChevronUp, ChevronDown, ZoomIn, ZoomOut, RotateCcw } from 'lucide-react';

// Dynamically import react-pdf components to avoid SSR issues
const Document = dynamic(() => import('react-pdf').then(mod => ({ default: mod.Document })), { 
  ssr: false,
  loading: () => (
    <div className="flex items-center justify-center h-full">
      <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
    </div>
  )
});

const Page = dynamic(() => import('react-pdf').then(mod => ({ default: mod.Page })), { 
  ssr: false 
});

// Import CSS styles for react-pdf (only on client side)
if (typeof window !== 'undefined') {
  import('react-pdf/dist/Page/AnnotationLayer.css');
  import('react-pdf/dist/Page/TextLayer.css');
}

interface PDFViewerProps {
  file: File | string | null;
  className?: string;
}

export default function PDFViewer({ file, className = '' }: PDFViewerProps) {
  const [numPages, setNumPages] = useState<number>(0);
  const [scale, setScale] = useState<number>(0.8);
  const [rotation, setRotation] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [workerReady, setWorkerReady] = useState<boolean>(false);
  const [retryCount, setRetryCount] = useState<number>(0);

  // Debug file prop
  useEffect(() => {
    console.log('PDFViewer: File prop changed:', {
      file,
      type: typeof file,
      isFile: file instanceof File,
      name: file instanceof File ? file.name : 'N/A',
      size: file instanceof File ? file.size : 'N/A'
    });
  }, [file]);

  // Configure PDF.js worker on client side only
  useEffect(() => {
    let mounted = true;
    
    if (typeof window !== 'undefined') {
      console.log('PDFViewer: Setting up PDF.js worker..., retryCount:', retryCount);

      const setupWorker = async () => {
        try {
          const pdfModule = await import('react-pdf');
          
          // Only proceed if component is still mounted
          if (!mounted) return;
          
          // Always reconfigure on retry
          if (retryCount === 0 && pdfModule.pdfjs.GlobalWorkerOptions.workerSrc) {
            console.log('PDFViewer: Worker already configured:', pdfModule.pdfjs.GlobalWorkerOptions.workerSrc);
            setWorkerReady(true);
            return;
          }
          
          // Use CDN worker for reliability
          const workerSrc = 'https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js';
          pdfModule.pdfjs.GlobalWorkerOptions.workerSrc = workerSrc;
          console.log('PDFViewer: Worker source set to:', workerSrc);
          
          if (mounted) {
            setWorkerReady(true);
            console.log('PDFViewer: Worker is ready');
          }
        } catch (error) {
          console.error('PDFViewer: Failed to setup worker:', error);
          if (mounted) {
            setError('Failed to initialize PDF viewer');
          }
        }
      };
      
      // Add small delay to ensure proper re-initialization on retry
      const delay = retryCount > 0 ? 300 : 0;
      setTimeout(setupWorker, delay);
    }
    
    return () => {
      mounted = false;
    };
  }, [retryCount]);

  const onDocumentLoadSuccess = useCallback(({ numPages }: { numPages: number }) => {
    console.log('PDFViewer: Document loaded successfully with', numPages, 'pages');
    setNumPages(numPages);
    setIsLoading(false);
    setError(null);
  }, []);

  const onDocumentLoadError = useCallback((error: Error) => {
    console.error('PDFViewer: Document loading error:', error);
    console.error('PDFViewer: Error details:', {
      message: error.message,
      name: error.name,
      stack: error.stack
    });
    setError(`Failed to load PDF: ${error.message}`);
    setIsLoading(false);
  }, []);


  const handleZoomIn = () => {
    setScale(prev => Math.min(3.0, prev + 0.25));
  };

  const handleZoomOut = () => {
    setScale(prev => Math.max(0.5, prev - 0.25));
  };

  const handleRotate = () => {
    setRotation(prev => (prev + 90) % 360);
  };

  const handleResetView = () => {
    setScale(0.8);
    setRotation(0);
  };

  if (!file) {
    return (
      <div className={`flex items-center justify-center bg-background border border-custom rounded-lg ${className}`}>
        <div className="text-center text-muted p-8">
          <p className="text-sm">No PDF file selected</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`flex flex-col bg-background border border-custom rounded-lg ${className}`}>
      {/* PDF Controls */}
      <div className="flex items-center justify-between p-2 border-b border-custom bg-surface shrink-0">
        <div className="flex items-center gap-2">
          <span className="text-xs text-muted px-2">
            {numPages} {numPages === 1 ? 'page' : 'pages'}
          </span>
        </div>

        <div className="flex items-center gap-1">
          <button
            onClick={handleZoomOut}
            disabled={scale <= 0.5}
            className="p-1 rounded hover:bg-background disabled:opacity-50 disabled:cursor-not-allowed"
            title="Zoom out"
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          <span className="text-xs text-muted px-2">
            {Math.round(scale * 100)}%
          </span>
          <button
            onClick={handleZoomIn}
            disabled={scale >= 3.0}
            className="p-1 rounded hover:bg-background disabled:opacity-50 disabled:cursor-not-allowed"
            title="Zoom in"
          >
            <ZoomIn className="w-4 h-4" />
          </button>
          <button
            onClick={handleRotate}
            className="p-1 rounded hover:bg-background"
            title="Rotate"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* PDF Document Display */}
      <div className="flex-1 overflow-auto p-2 bg-gray-50 min-h-0">
        {(!workerReady || isLoading) && (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
              <p className="text-sm text-muted">{!workerReady ? 'Initializing PDF viewer...' : 'Loading PDF...'}</p>
            </div>
          </div>
        )}

        {error && (
          <div className="flex items-center justify-center h-full">
            <div className="text-center text-red-500">
              <p className="text-sm">{error}</p>
              <button
                onClick={() => {
                  setError(null);
                  setIsLoading(true);
                  setWorkerReady(false);
                  setRetryCount(prev => prev + 1);
                }}
                className="mt-2 text-xs text-primary hover:underline"
              >
                Try again {retryCount > 0 && `(${retryCount + 1})`}
              </button>
            </div>
          </div>
        )}

        {!isLoading && !error && workerReady && (
          <Document
            file={file}
            onLoadSuccess={onDocumentLoadSuccess}
            onLoadError={onDocumentLoadError}
            onLoadStart={() => {
              console.log('PDFViewer: Document load started for file:', file);
              setIsLoading(true);
            }}
            onLoadProgress={({ loaded, total }) => {
              console.log('PDFViewer: Loading progress:', Math.round((loaded / total) * 100), '%');
            }}
            loading={
              <div className="flex items-center justify-center h-full">
                <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
              </div>
            }
            className="flex flex-col items-center"
          >
            <div className="space-y-4">
              {Array.from(new Array(numPages), (el, index) => (
                <div key={`page_${index + 1}`} className="border border-gray-300 shadow-lg">
                  <Page
                    pageNumber={index + 1}
                    scale={scale}
                    rotate={rotation}
                    loading={
                      <div className="flex items-center justify-center h-40 bg-white">
                        <div className="w-6 h-6 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
                      </div>
                    }
                    renderTextLayer={false}
                    renderAnnotationLayer={false}
                    className="max-w-full"
                  />
                </div>
              ))}
            </div>
          </Document>
        )}
      </div>

      {/* Quick Navigation */}
      {numPages > 0 && (
        <div className="p-2 border-t border-custom bg-surface shrink-0">
          <div className="flex items-center justify-between">
            <button
              onClick={handleResetView}
              className="text-xs text-primary hover:underline"
            >
              Reset View
            </button>
            <div className="text-xs text-muted">
              {numPages} page{numPages !== 1 ? 's' : ''}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
