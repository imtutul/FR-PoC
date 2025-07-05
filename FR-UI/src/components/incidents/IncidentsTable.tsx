"use client";
import React from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHeader,
  TableRow,
} from "../ui/table";

import Badge from "../ui/badge/Badge";
import Image from "next/image";
import Incident from "@/types/incidents/incident";
import { AssociateCount } from "./AssociateCount";
import MultiSelect from "../form/MultiSelect";
import { ArrowRightIcon } from "@/icons";
import Button from "../ui/button/Button";

const tableData: Incident[] = [
  {
    id: 1,
    incidentId: "OCT 01 1000001",
    dateTime: new Date("2023-10-01T10:00:00Z"),
    accociates: [
      {
        id: 1,
        name: "John Doe",
        image: "/images/user/user-28.jpg",
        role: "Security Officer",
      },
    ],
    suspects: [
      {
        id: 1,
        name: "Suspect A",
        image: "/images/user/user-22.jpg",
        role: "Suspect",
      },
      {
        id: 2,
        name: "Suspect B",
        image: "/images/user/user-23.jpg",
        role: "Suspect",
      },
    ],
    pois: [
      {
        id: 1,
        name: "POI A",
        image: "/images/user/user-24.jpg",
        role: "Point of Interest",
      },
      {
        id: 2,
        name: "POI B",
        image: "/images/user/user-25.jpg",
        role: "Point of Interest",
      },
    ],
    numberOfDetections: 5,
    images: [
      "/images/user/user-22.jpg",
      "/images/user/user-23.jpg",
    ],
  },
  {
    id: 2,
    incidentId: "OCT 02 1000002",
    dateTime: new Date("2023-10-02T11:30:00Z"),
    accociates: [
      {
        id: 2,
        name: "Jane Smith",
        image: "/images/user/user-31.jpg",
        role: "Security Officer",
      },
      {
        id: 3,
        name: "Alice Johnson",
        image: "/images/user/user-21.jpg",
        role: "Security Officer",
      },
      {
        id: 4,
        name: "Bob Brown",
        image: "/images/user/user-24.jpg",
        role: "Security Officer",
      },
      {
        id: 5,
        name: "Charlie Davis",
        image: "/images/user/user-25.jpg",
        role: "Security Officer",
      },
      {
        id: 6,
        name: "Eve White",
        image: "/images/user/user-26.jpg",
        role: "Security Officer",
      }
    ],
    suspects: [
      {
        id: 1,
        name: "Suspect C",
        image: "/images/user/user-22.jpg",
        role: "Suspect",
      }
    ],
    pois: [
      {
        id: 1,
        name: "POI C",
        image: "/images/user/user-23.jpg",
        role: "Point of Interest",
      },
      {
        id: 2,
        name: "POI D",
        image: "/images/user/user-24.jpg",
        role: "Point of Interest",
      },
      {
        id: 3,
        name: "POI E",
        image: "/images/user/user-25.jpg",
        role: "Point of Interest",
      },
      {
        id: 4,
        name: "POI F",
        image: "/images/user/user-26.jpg",
        role: "Point of Interest",
      },
    ],
    numberOfDetections: 3,
    images: [
      "/images/user/user-24.jpg",
      "/images/user/user-25.jpg",
      "/images/user/user-25.jpg",
      "/images/user/user-25.jpg",
      "/images/user/user-25.jpg",
      "/images/user/user-25.jpg",
    ],
  },
  {
    id: 3,
    incidentId: "OCT 03 1000003",
    dateTime: new Date("2023-10-03T09:15:00Z"),
    accociates: [
      {
        id: 3,
        name: "Alice Johnson",
        image: "/images/user/user-21.jpg",
        role: "Security Officer",
      },
    ],
    suspects: [
      {
        id: 2,
        name: "Suspect D",
        image: "/images/user/user-22.jpg",
        role: "Suspect",
      },
    ],
    pois: [
      {
        id: 3,
        name: "POI G",
        image: "/images/user/user-23.jpg",
        role: "Point of Interest",
      },
      {
        id: 4,
        name: "POI H",
        image: "/images/user/user-24.jpg",
        role: "Point of Interest",
      },
    ],
    numberOfDetections: 4,
    images: [
      "/images/user/user-25.jpg",
      "/images/user/user-26.jpg",
    ],
  },
];

const zoneOptions = [
  { value: "zone0", text: "Zone 0",selected: false },
  { value: "zone1", text: "Zone 1",selected: false},
  { value: "zone2", text: "Zone 2",selected: false},
  { value: "zone3", text: "Zone 3",selected: false},
];

const handleZoneChange = (event:any) => {
  console.log("Selected Zone:", event);
};

const cameraOptions = [
  { value: "camera1", text: "Camera 1",selected: false },
  { value: "camera2", text: "Camera 2",selected: false},
  { value: "camera3", text: "Camera 3",selected: false },
];

const handleCameraChange = (event:any) => {
  console.log("Selected Camera:", event);
};

const poiOptions = [
  { value: "poi1", text: "POI 1",selected: false },
  { value: "poi2", text: "POI 2",selected: false},
  { value: "poi3", text: "POI 3",selected: false },
];

const handlePoiChange = (event:any) => {
  console.log("Selected POI:", event);
};

const suspectOptions = [
  { value: "suspect1", text: "Suspect 1",selected: false },
  { value: "suspect2", text: "Suspect 2",selected: false},
  { value: "suspect3", text: "Suspect 3",selected: false },
];

const handleSuspectChange = (event:any) => {
  console.log("Selected Suspect:", event);
};

const employeeOptions = [
  { value: "employee1", text: "Employee 1",selected: false },
  { value: "employee2", text: "Employee 2",selected: false},
  { value: "employee3", text: "Employee 3",selected: false },
];

const handleEmployeeChange = (event:any) => {
  console.log("Selected Employee:", event);
};

export default function IncidentsTable() {
  return (
    <div>
      <div className="rounded-xl border border-gray-200 bg-white dark:border-white/[0.05] dark:bg-white/[0.03] margin-bottom-4">
      <div className="grid grid-cols-4 gap-4 p-3">
        <div className="relative">
          <MultiSelect
            placeholder="Select zone"
            options={zoneOptions}
            onChange={(values) => handleCameraChange(values)}
          />
        </div>
          
        <div className="relative">
          <MultiSelect
            options={cameraOptions}
            placeholder="Select camera"
            onChange={handleCameraChange}
          />
        </div>
          
        <div className="relative">
          <MultiSelect
            options={poiOptions}
            placeholder="Select POI"
            onChange={handlePoiChange}
          />
        </div>
          
        <div className="relative">
          <MultiSelect
            options={suspectOptions}
            placeholder="Select suspect"
            onChange={handleSuspectChange} 
          />
        </div>
        <div className="relative">
          <MultiSelect
            options={employeeOptions}
            placeholder="Select employee"
            onChange={handleEmployeeChange}
          />
        </div>
          
        <Button className="h-11">
          <div className="flex items-center justify-between">
            <span className="text-sm">Go</span>
            <span>
              <ArrowRightIcon />
            </span>
          </div>
        </Button>
      </div>
      </div>
      <div className="overflow-hidden rounded-xl border border-gray-200 bg-white dark:border-white/[0.05] dark:bg-white/[0.03]">
        <div className="max-w-full overflow-x-auto">
          <div className="min-w-[1102px]">
            <Table>
              {/* Table Header */}
              <TableHeader className="border-b border-gray-100 dark:border-white/[0.05]">
                <TableRow>
                  <TableCell
                    isHeader
                    className="px-5 py-3 font-medium text-gray-500 text-start text-theme-xs dark:text-gray-400"
                  >
                    <div className="flex items-center justify-center">
                      Incident ID
                    </div>  
                  </TableCell>
                  <TableCell
                    isHeader
                    className="px-5 py-3 font-medium text-gray-500 text-start text-theme-xs dark:text-gray-400"
                  >
                    <div className="flex items-center justify-center">
                      Date & Time
                    </div>
                  </TableCell>
                  <TableCell
                    isHeader
                    className="px-5 py-3 font-medium text-gray-500 text-start text-theme-xs dark:text-gray-400"
                  >
                    <div className="flex items-center">
                      Images
                    </div>
                  </TableCell>
                  <TableCell
                    isHeader
                    className="px-5 py-3 font-medium text-gray-500 text-start text-theme-xs dark:text-gray-400"
                  >
                    <div className="flex items-center justify-center">
                      Associates
                    </div>
                  </TableCell>
                  <TableCell
                    isHeader
                    className="px-5 py-3 font-medium text-gray-500 text-start text-theme-xs dark:text-gray-400"
                  >
                    <div className="flex items-center justify-center">
                      Number of Detections
                    </div>
                  </TableCell>
                  <TableCell
                    isHeader
                    className="px-5 py-3 font-medium text-gray-500 text-start text-theme-xs dark:text-gray-400"
                  >
                    <div className="flex items-center justify-center">
                      Actions
                    </div>
                  </TableCell>
                </TableRow>
              </TableHeader>

              {/* Table Body */}
              <TableBody className="divide-y divide-gray-100 dark:divide-white/[0.05]">
                {tableData.map((incident) => (
                  <TableRow key={incident.id}>
                    <TableCell className="px-5 py-4 sm:px-6 text-start text-gray-500 text-theme-sm dark:text-gray-400">
                      <div className="flex items-center justify-center">
                        {incident.incidentId}
                      </div>
                    </TableCell>
                    <TableCell className="px-4 py-3 text-gray-500 text-start text-theme-sm dark:text-gray-400">
                      <div className="flex items-center justify-center">
                        {incident.dateTime.toLocaleString()}
                      </div>
                    </TableCell>
                    <TableCell className="px-4 py-3 text-gray-500 text-start text-theme-sm dark:text-gray-400">
                      <div className="flex">
                        {incident.images.map((teamImage, index) => (
                          <div
                            key={index}
                            className="w-10 h-10 overflow-hidden border-2 border-white rounded dark:border-gray-900"
                          >
                            <Image
                              width={24}
                              height={24}
                              src={teamImage}
                              alt={`Team member ${index + 1}`}
                              className="w-full"
                            />
                          </div>
                        ))}
                      </div>
                    </TableCell>
                    <TableCell className="px-4 py-3 text-gray-500 text-start text-theme-sm dark:text-gray-400">
                      <AssociateCount
                        associates={incident.accociates}
                        suspects={incident.suspects}
                        pois={incident.pois}
                      />
                    </TableCell>
                    <TableCell className="px-4 py-3 text-gray-500 text-theme-sm dark:text-gray-400">
                      <div className="flex items-center justify-center">
                        {incident.numberOfDetections}
                      </div>
                    </TableCell>
                    <TableCell className="px-4 py-3 text-gray-500 text-start text-theme-sm dark:text-gray-400">
                      <Badge color="primary" >
                        View Details
                      </Badge>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </div>
        </div>
    </div>
  );
}
