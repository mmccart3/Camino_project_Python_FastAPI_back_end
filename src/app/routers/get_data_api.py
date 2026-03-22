from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import json

router = APIRouter()

from ..db.db_connect import connect_to_db
print("IN GET DATA API")
dbconnection = connect_to_db()


@router.get("/albergue", status_code=200)
async def get_albergue_data():
    global dbconnection
    print("In get_data endpoint")
    try:
        SQL_command = ("""SELECT
            albergue.ID AS ID,
            albergueName AS name,
            numberOfBeds AS beds,
            numberOfDorms AS dorms,
            albergueStreetAdress AS address,
            onedPersonRateMin AS rate,
            kitchenFacilitiesAvailable AS kitchen,
            washingMachineAvailable AS washingMachine,
            dryingMachineAvailable AS dryer,
            communalMealAvailable AS meal,
            openingPeriod,
            email,
            tel1CountryCode AS crtyCode,
            tel1PhoneNumber AS phone,
            albergueWebsiteURL AS URL,
            albergueBookingDotComURL AS booking,
            albergueAdditionalComments AS comments,
            alberguepic1URL AS pic1,
            alberguepic2URL AS pic2,
            alberguepic3URL AS pic3,
            alberguepic4URL AS pic4,
            whatsAppNumber,
            gps_lat,
            gps_lng,
            check_in_opens AS opens,
            check_in_closes AS closes,
            locationID AS locID,
            locationName AS locations
            FROM albergue, locations 
            WHERE locations.ID = locationID;
            """)
        mycursor = dbconnection.cursor(dictionary=True)
        mycursor.execute(SQL_command)
        print("Executed albergue query")
        data = mycursor.fetchall()
        return data
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/stage", status_code=200)
async def get_stage_data():
    global dbconnection
    try:
        SQL_command = ("""
                       SELECT JSON_ARRAY(JSON_OBJECT(
                            "ID",  s.id,
                            "stageName",  s.stageName,
                            "stageDistanceInMetres",  s.stageDistanceInMetres,
                            "stageTimeInMinutes", s.stageTimeInMinutes,
                            "stageStartLocationID",  s.stageStartLocationID,
                            "stageFinishLocationID",  s.stageFinishLocationID,
                            "stageMapURL",  s.stageMapURL,
                            "stageElevationChartURL",  s.stageElevationChartURL,
							"Locations",(SELECT JSON_ARRAYAGG(JSON_OBJECT(
                                "ID", locs.ID,
                                "locationName", locs.locationName,
                                "latitude", locs.latitude,
                                "longitude", locs.longitude,
                                "locationPic1URL", locs.locationPic1URL,
                                "locationPic2URL", locs.locationPic2URL,
                                "locationPic3URL", locs.locationPic3URL,
                                "locationPic4URL", locs.locationPic4URL,
                                "priorLoc", locs.priorLoc,
                                "nextLoc", locs.nextLoc,
                                "altPriorLoc", locs.altPriorLoc,
                                "altNextLoc", locs.altNextLoc,
                                "Stage2locations",
                                (SELECT JSON_ARRAYAGG(JSON_OBJECT(
                                    "distanceFromPriorLocationInMetres", S2L.distanceFromPriorLocationInMetres,
                                    "timeFromPriorLocationInMinutes", S2L.timeFromPriorLocationInMinutes,
                                    "stageID", S2L.stageID,
                                    "locationID", S2L.locationID))
                                        FROM stages2locations AS S2L
                                        WHERE S2L.stageID = s.ID
                                        AND S2L.locationID = locs.ID)
                                )) AS Locations
                            FROM  (SELECT 
                                locations.ID,
                                locationName,
                                latitude,
                                longitude,
                                locationPic1URL,
                                locationPic2URL,
                                locationPic3URL,
                                locationPic4URL,
                                priorLoc,
                                nextLoc,
                                altPriorLoc,
                                altNextLoc FROM 
                                locations, stages2locations, stages
                                WHERE locations.ID = stages2locations.locationID
                                AND stages.ID = stages2locations.stageID
                                AND stages.ID = s.ID) AS locs)))
                                AS stageData FROM stages s
                            ;
                            """)
        mycursor = dbconnection.cursor(dictionary=True)
        mycursor.execute(SQL_command)
        data = mycursor.fetchall()
        for row in data:
            if row.get("Locations"):
                row["Locations"] = json.loads(row["Locations"])
            if row.get("stageData"):
                row["stageData"] = json.loads(row["stageData"])
        return data
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/stage2", status_code=200)
async def get_stage_data2():
    global dbconnection
    print("In get_data endpoint")
    try:
        SQL_command = ("""SELECT ID FROM stages;""")
        mycursor = dbconnection.cursor(dictionary=False)
        mycursor.execute(SQL_command)
        stage_ids = mycursor.fetchall()
        print(stage_ids)
        stage_list = []
        for stages in stage_ids:
            stage_list.append(stages[0])
        print(stage_list)
        data = []
        for stage_id in stage_list: #
            print(stage_id)
            SQL_command = ("""
                select s.ID,s.stageName,
                stageDistanceInMetres,
                stageTimeInMinutes,
                stageStartLocationID,
                stageFinishLocationID,
                stageMapURL,
                stageElevationChartURL,
                    JSON_ARRAYAGG(
                        JSON_OBJECT(
                        "locationName", locs.locationName,
                        "latitude", locs.latitude,
                        "longitude", locs.longitude,
                        "locationPic1URL", locs.locationPic1URL,
                        "locationPic2URL", locs.locationPic2URL,
                        "locationPic3URL", locs.locationPic3URL,
                        "locationPic4URL", locs.locationPic4URL,
                        "priorLoc", locs.priorLoc,
                        "nextLoc", locs.nextLoc,
                        "altPriorLoc", locs.altPriorLoc,
                        "altNextLoc", locs.altNextLoc,
                        "stageID", locs.stageID,
                        "locationID", locs.locationID,
                        "distanceFromPriorLocationInMetres", locs.distanceFromPriorLocationInMetres,
                        "timeFromPriorLocationInMinutes", locs.timeFromPriorLocationInMinutes
                        )) as Locations
                        from  (select 
                        locations.ID,
                        locationName,
                        latitude,
                        longitude,
                        locationPic1URL,
                        locationPic2URL,
                        locationPic3URL,
                        locationPic4URL,
                        priorLoc,
                        nextLoc,
                        altPriorLoc,
                        altNextLoc,
                        stages2locations.locationID,
                        stageID,
                        stages2locations.distanceFromPriorLocationInMetres,
                        stages2locations.timeFromPriorLocationInMinutes
                        from 
                        locations, stages2locations, stages
                        where locations.ID = stages2locations.locationID
                        and 
                        stages.ID = stages2locations.stageID
                        and stages.ID = %s ) as locs,  stages as s
                        where 
                        s.ID = %s
                        """)
            mycursor = dbconnection.cursor(dictionary=True)
            params = {"stage_id": stage_id}
            print(params)
            # Example of how to use params if needed:
    
            mycursor.execute(SQL_command, (stage_id, stage_id))
            print ("Executed stage query")
            temp_data = mycursor.fetchall()
            for row in temp_data:
                if row.get("Locations"):
                    row["Locations"] = json.loads(row["Locations"])
                else:
                    row["Locations"] = []
            data.append(temp_data)
        return data
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
        
@router.get("/stageData", status_code=200)
async def get_stage_data():
    global dbconnection
    print("In get_data endpoint")
    try:
        SQL_command = ("""SELECT stages.ID AS "StageID", stageName, fromloc.locationName AS "from", toloc.locationName AS "to",
            distanceFromPriorLocationInMetres, timeFromPriorLocationInMinutes, priorStage, altPriorStage, nextStage, altNextStage
            FROM stageDetails, stages, locations as fromloc, locations as toloc
            WHERE stageDetails.stageID = stages.ID
            AND fromLocationID = fromloc.ID
            AND toLocationId = toloc.ID
            ORDER BY stages.ID ASC;
            """)
        mycursor = dbconnection.cursor(dictionary=True)
        mycursor.execute(SQL_command)
        data = mycursor.fetchall()
        return data
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
        
@router.get("/locations", status_code=200)
async def get_location_data():
    global dbconnection
    print("In get_data endpoint")
    try:
        SQL_command = ("""
                       SELECT * FROM locations;
            """)
        mycursor = dbconnection.cursor(dictionary=True)
        mycursor.execute(SQL_command)
        data = mycursor.fetchall()
        return data
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
        
@router.get("/coords", status_code=200)
async def get_maps_coords_data():
    global dbconnection
    print("In get_data endpoint")
    try:
        SQL_command = ("""
                       SELECT * FROM mapLocationCoords;
            """)
        mycursor = dbconnection.cursor(dictionary=True)
        mycursor.execute(SQL_command)
        data = mycursor.fetchall()
        return data
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
        
        
        
@router.get("/privateAccomm", status_code=200)
async def get_private_accomm_data():
    global dbconnection
    print("In get_data endpoint")
    try:
        SQL_command = ("""
                        SELECT 
                        privateAccommDetail.ID AS ID,
                        privateAccommName AS Name,
                        privateAccommStreetAdress AS address,
                        onedPersonRateMin AS OnePrate,
                        twoPersonRateMin AS TwoPrate,
                        tel1CountryCode AS ctryCode,
                        tel1PhoneNumber AS tel,
                        privateAccommWebsiteURL AS URL,
                        privateAccommBookingDotComURL AS booking,
                        gps_lat AS lat,
                        gps_lng AS lng,
                        locationID AS locID,
                        locationName AS location 
                        FROM privateAccommDetail, locations 
                        WHERE locations.ID = locationID;
            """)
        mycursor = dbconnection.cursor(dictionary=True)
        mycursor.execute(SQL_command)
        data = mycursor.fetchall()
        return data
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )