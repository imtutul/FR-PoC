"use client";
import React from "react";
import Badge from "../ui/badge/Badge";
import { AlertIcon, EyeCloseIcon, EyeIcon, GroupIcon, UserIcon } from "@/icons";

export const IncidentMetrics = () => {
  return (
    <div className="grid grid-cols-3 gap-4 md:gap-6">
      <div className="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03] md:p-6">
        <div className="flex items-center justify-center w-12 h-12 bg-gray-100 rounded-xl dark:bg-gray-800">
          <AlertIcon className="text-amber-600 size-6 dark:text-amber-200" />
        </div>

        <div className="flex items-end justify-between mt-5">
            <div>
                <span className="text-lg text-gray-500 dark:text-gray-400">
                    Total incident detected
                </span>
            </div>
            <h4 className="font-bold text-gray-800 text-title-sm dark:text-white/90">
              3,782
            </h4>
        </div>
      </div>
      
      <div className="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03] md:p-6">
        <div className="flex items-center justify-center w-12 h-12 bg-gray-100 rounded-xl dark:bg-gray-800">
          <UserIcon className="text-red-600 size-6 dark:text-error-300" />
        </div>

        <div className="flex items-end justify-between mt-5">
            <div>
                <span className="text-lg text-gray-500 dark:text-gray-400">
                    Total number of suspects
                </span>
            </div>
            <h4 className="font-bold text-gray-800 text-title-sm dark:text-white/90">
              3,782
            </h4>
        </div>
          </div>
          
          <div className="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03] md:p-6">
        <div className="flex items-center justify-center w-12 h-12 bg-gray-100 rounded-xl dark:bg-gray-800">
          <GroupIcon className="text-green-800 size-6 dark:text-green-300" />
        </div>

        <div className="flex items-end justify-between mt-5">
            <div>
                <span className="text-lg text-gray-500 dark:text-gray-400">
                    Total associate count
                </span>
            </div>
            <h4 className="font-bold text-gray-800 text-title-sm dark:text-white/90">
              3,782
            </h4>
        </div>
      </div>
    </div>
  );
};
