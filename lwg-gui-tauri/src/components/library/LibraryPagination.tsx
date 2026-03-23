// src/components/library/LibraryPagination.tsx
import { memo, useCallback } from "react";
import { Input } from "@/components/ui/input";
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { toast } from "sonner";

interface LibraryPaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export const LibraryPagination = memo(
  ({ currentPage, totalPages, onPageChange }: LibraryPaginationProps) => {
    // 智能页码生成逻辑 (1 ... 4 5 6 ... 20)
    const getPageNumbers = useCallback(() => {
      const pages: (number | string)[] = [];

      if (totalPages <= 7) {
        for (let i = 1; i <= totalPages; i++) pages.push(i);
      } else {
        if (currentPage <= 4) {
          for (let i = 1; i <= 5; i++) pages.push(i);
          pages.push("...");
          pages.push(totalPages);
        } else if (currentPage >= totalPages - 3) {
          pages.push(1);
          pages.push("...");
          for (let i = totalPages - 4; i <= totalPages; i++) pages.push(i);
        } else {
          pages.push(1);
          pages.push("...");
          for (let i = currentPage - 1; i <= currentPage + 1; i++)
            pages.push(i);
          pages.push("...");
          pages.push(totalPages);
        }
      }
      return pages;
    }, [currentPage, totalPages]);

    const handleJumpToPage = (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === "Enter") {
        const target = parseInt(e.currentTarget.value);
        if (!isNaN(target) && target >= 1 && target <= totalPages) {
          onPageChange(target);
          e.currentTarget.value = "";
        } else {
          toast.error("Invalid Page", {
            description: `Please enter a number between 1 and ${totalPages}`,
          });
        }
      }
    };

    if (totalPages <= 1) return null;

    return (
      <div className="mt-8 pb-4 flex items-center justify-center gap-4">
        <Pagination className="mx-0 w-auto">
          <PaginationContent>
            <PaginationItem>
              <PaginationPrevious
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  onPageChange(currentPage - 1);
                }}
                className={
                  currentPage === 1
                    ? "pointer-events-none opacity-50"
                    : "cursor-pointer"
                }
              />
            </PaginationItem>

            {getPageNumbers().map((page, index) => (
              <PaginationItem key={index}>
                {page === "..." ? (
                  <PaginationEllipsis />
                ) : (
                  <PaginationLink
                    href="#"
                    isActive={page === currentPage}
                    onClick={(e) => {
                      e.preventDefault();
                      onPageChange(page as number);
                    }}
                    className="cursor-pointer"
                  >
                    {page}
                  </PaginationLink>
                )}
              </PaginationItem>
            ))}

            <PaginationItem>
              <PaginationNext
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  onPageChange(currentPage + 1);
                }}
                className={
                  currentPage === totalPages
                    ? "pointer-events-none opacity-50"
                    : "cursor-pointer"
                }
              />
            </PaginationItem>
          </PaginationContent>
        </Pagination>

        {totalPages > 7 && (
          <div className="flex items-center gap-2 text-sm text-muted-foreground ml-2 border-l pl-4 h-5">
            <span>Go to</span>
            <div className="relative">
              <Input
                type="number"
                min={1}
                max={totalPages}
                className="h-8 w-14 text-center px-0 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none focus-visible:ring-1"
                onKeyDown={handleJumpToPage}
                placeholder={currentPage.toString()}
              />
            </div>
            <span>of {totalPages}</span>
          </div>
        )}
      </div>
    );
  },
);

LibraryPagination.displayName = "LibraryPagination";
