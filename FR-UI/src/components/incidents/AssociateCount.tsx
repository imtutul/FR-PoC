import { AssociateIcon, POIIcon, SuspectIcon } from "@/icons";
import { Associate } from "@/types/incidents/Associate";
import { POI } from "@/types/incidents/POI";
import { Suspect } from "@/types/incidents/Suspect";
import React, { use, useEffect } from "react";

type AssociateCountProps = {
  associates?: Associate[];
  suspects?: Suspect[];
  pois?: POI[];
};

export const AssociateCount = ({ associates,suspects,pois }: AssociateCountProps) => {
    
    return (
      <div className="flex flex-col space-y-4">
        {associates && associates.length > 0 && (
          <div className="flex items-center justify-between">
            <div className="flex flex-row flex-wrap">
              {associates.map((associate) => (
                <div key={associate.id} >
                  <AssociateIcon className="w-3" />
                </div>
              ))}
            </div>
            <div>
              {associates.length > 0 && (
                <span className="text-cyan-400 dark:text-cyan-400">
                  {associates.length}
                </span>
              )}
            </div>
          </div>
        )}

        {suspects && suspects.length > 0 && (
          <div className="flex items-center justify-between">
            <div className="flex flex-row flex-wrap">
              {suspects && suspects.map((suspect) => (
                <div key={suspect.id} >
                  <SuspectIcon className="w-3" />
                </div>
              ))}
            </div>
            <div>
              {suspects && suspects.length > 0 ? (
                <span className="text-pink-500 dark:text-pink-500"> 
                  {suspects.length}
                </span>
              ) : null}
            </div>
          </div>
        )}

        {pois && pois.length > 0 &&  (
          <div className="flex items-center justify-between">
          <div className="flex flex-row flex-wrap">
            {pois && pois.map((poi) => (
              <div key={poi.id} >
                <POIIcon className="w-3" />
              </div>
            ))}
          </div>
          <div>
            {pois && pois.length > 0 && (
              <span className="text-amber-500 dark:text-amber-500"> 
                {pois.length}
              </span>
            )}
          </div>
          </div>
        )}
      </div>
  );
}