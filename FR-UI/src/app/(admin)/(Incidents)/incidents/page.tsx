import { IncidentMetrics } from "@/components/incidents/IncidentMetrics";
import IncidentsTable from "@/components/incidents/IncidentsTable";
import BasicTableOne from "@/components/tables/BasicTableOne";
import { Metadata } from "next";
import React from "react";

export const metadata: Metadata = {
  title: "DCH Face Recognition | Incidents",
  description: "This is the incidents page of the DCH Face Recognition system.",
};

export default function Incidents() {
  return (
    <div className="grid grid-cols-12 gap-4 md:gap-6">
      {/* <div className="col-span-12 space-y-6 xl:col-span-12">
        <IncidentMetrics />
      </div> */}
      <div className="col-span-12 space-y-6 xl:col-span-12">

      </div>  
      <div className="col-span-12 xl:col-span-12">
        <IncidentsTable />
      </div>  
    </div>  
  );
}
