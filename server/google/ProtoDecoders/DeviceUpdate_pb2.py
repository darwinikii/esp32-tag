# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ProtoDecoders/DeviceUpdate.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ProtoDecoders import Common_pb2 as ProtoDecoders_dot_Common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n ProtoDecoders/DeviceUpdate.proto\x1a\x1aProtoDecoders/Common.proto\"g\n GetEidInfoForE2eeDevicesResponse\x12\x43\n\x1c\x65ncryptedOwnerKeyAndMetadata\x18\x04 \x01(\x0b\x32\x1d.EncryptedOwnerKeyAndMetadata\"j\n\x1c\x45ncryptedOwnerKeyAndMetadata\x12\x19\n\x11\x65ncryptedOwnerKey\x18\x01 \x01(\x0c\x12\x17\n\x0fownerKeyVersion\x18\x02 \x01(\x05\x12\x16\n\x0esecurityDomain\x18\x03 \x01(\t\"6\n\x0b\x44\x65vicesList\x12\'\n\x0e\x64\x65viceMetadata\x18\x02 \x03(\x0b\x32\x0f.DeviceMetadata\"R\n\x12\x44\x65vicesListRequest\x12<\n\x18\x64\x65viceListRequestPayload\x18\x01 \x01(\x0b\x32\x1a.DevicesListRequestPayload\"B\n\x19\x44\x65vicesListRequestPayload\x12\x19\n\x04type\x18\x01 \x01(\x0e\x32\x0b.DeviceType\x12\n\n\x02id\x18\x03 \x01(\t\"\x96\x01\n\x14\x45xecuteActionRequest\x12\"\n\x05scope\x18\x01 \x01(\x0b\x32\x13.ExecuteActionScope\x12\"\n\x06\x61\x63tion\x18\x02 \x01(\x0b\x32\x12.ExecuteActionType\x12\x36\n\x0frequestMetadata\x18\x03 \x01(\x0b\x32\x1d.ExecuteActionRequestMetadata\"\xaf\x01\n\x1c\x45xecuteActionRequestMetadata\x12\x19\n\x04type\x18\x01 \x01(\x0e\x32\x0b.DeviceType\x12\x13\n\x0brequestUuid\x18\x02 \x01(\t\x12\x15\n\rfmdClientUuid\x18\x03 \x01(\t\x12\x37\n\x11gcmRegistrationId\x18\x04 \x01(\x0b\x32\x1c.GcmCloudMessagingIdProtobuf\x12\x0f\n\x07unknown\x18\x06 \x01(\x08\")\n\x1bGcmCloudMessagingIdProtobuf\x12\n\n\x02id\x18\x01 \x01(\t\"\xa4\x01\n\x11\x45xecuteActionType\x12\x36\n\rlocateTracker\x18\x1e \x01(\x0b\x32\x1f.ExecuteActionLocateTrackerType\x12+\n\nstartSound\x18\x1f \x01(\x0b\x32\x17.ExecuteActionSoundType\x12*\n\tstopSound\x18  \x01(\x0b\x32\x17.ExecuteActionSoundType\"{\n\x1e\x45xecuteActionLocateTrackerType\x12*\n\x1blastHighTrafficEnablingTime\x18\x02 \x01(\x0b\x32\x05.Time\x12-\n\x0f\x63ontributorType\x18\x03 \x01(\x0e\x32\x14.SpotContributorType\"=\n\x16\x45xecuteActionSoundType\x12#\n\tcomponent\x18\x01 \x01(\x0e\x32\x10.DeviceComponent\"_\n\x12\x45xecuteActionScope\x12\x19\n\x04type\x18\x02 \x01(\x0e\x32\x0b.DeviceType\x12.\n\x06\x64\x65vice\x18\x03 \x01(\x0b\x32\x1e.ExecuteActionDeviceIdentifier\">\n\x1d\x45xecuteActionDeviceIdentifier\x12\x1d\n\tcanonicId\x18\x01 \x01(\x0b\x32\n.CanonicId\"\x96\x01\n\x0c\x44\x65viceUpdate\x12\x32\n\x0b\x66\x63mMetadata\x18\x01 \x01(\x0b\x32\x1d.ExecuteActionRequestMetadata\x12\'\n\x0e\x64\x65viceMetadata\x18\x03 \x01(\x0b\x32\x0f.DeviceMetadata\x12)\n\x0frequestMetadata\x18\x02 \x01(\x0b\x32\x10.RequestMetadata\"\xbd\x01\n\x0e\x44\x65viceMetadata\x12\x36\n\x15identifierInformation\x18\x01 \x01(\x0b\x32\x17.IdentitfierInformation\x12\'\n\x0binformation\x18\x04 \x01(\x0b\x32\x12.DeviceInformation\x12\x1d\n\x15userDefinedDeviceName\x18\x05 \x01(\t\x12+\n\x10imageInformation\x18\x06 \x01(\x0b\x32\x11.ImageInformation\"$\n\x10ImageInformation\x12\x10\n\x08imageUrl\x18\x01 \x01(\t\"\x90\x01\n\x16IdentitfierInformation\x12+\n\x10phoneInformation\x18\x01 \x01(\x0b\x32\x11.PhoneInformation\x12(\n\x04type\x18\x02 \x01(\x0e\x32\x1a.IdentifierInformationType\x12\x1f\n\ncanonicIds\x18\x03 \x01(\x0b\x32\x0b.CanonicIds\"3\n\x10PhoneInformation\x12\x1f\n\ncanonicIds\x18\x02 \x01(\x0b\x32\x0b.CanonicIds\"+\n\nCanonicIds\x12\x1d\n\tcanonicId\x18\x01 \x03(\x0b\x32\n.CanonicId\"\x17\n\tCanonicId\x12\n\n\x02id\x18\x01 \x01(\t\"\xa6\x01\n\x11\x44\x65viceInformation\x12/\n\x12\x64\x65viceRegistration\x18\x01 \x01(\x0b\x32\x13.DeviceRegistration\x12\x31\n\x13locationInformation\x18\x02 \x01(\x0b\x32\x14.LocationInformation\x12-\n\x11\x61\x63\x63\x65ssInformation\x18\x03 \x03(\x0b\x32\x12.AccessInformation\"<\n\x15\x44\x65viceTypeInformation\x12#\n\ndeviceType\x18\x02 \x01(\x0e\x32\x0f.SpotDeviceType\"\xd0\x01\n\x12\x44\x65viceRegistration\x12\x35\n\x15\x64\x65viceTypeInformation\x18\x02 \x01(\x0b\x32\x16.DeviceTypeInformation\x12\x33\n\x14\x65ncryptedUserSecrets\x18\x13 \x01(\x0b\x32\x15.EncryptedUserSecrets\x12\x14\n\x0cmanufacturer\x18\x14 \x01(\t\x12\x17\n\x0f\x66\x61stPairModelId\x18\x15 \x01(\t\x12\x10\n\x08pairDate\x18\x17 \x01(\x05\x12\r\n\x05model\x18\" \x01(\t\"\xb7\x01\n\x14\x45ncryptedUserSecrets\x12\x1c\n\x14\x65ncryptedIdentityKey\x18\x01 \x01(\x0c\x12\x17\n\x0fownerKeyVersion\x18\x03 \x01(\x05\x12\x1b\n\x13\x65ncryptedAccountKey\x18\x04 \x01(\x0c\x12\x1b\n\x0c\x63reationDate\x18\x08 \x01(\x0b\x32\x05.Time\x12.\n&encryptedSha256AccountKeyPublicAddress\x18\x0b \x01(\x0c\"F\n\x13LocationInformation\x12/\n\x07reports\x18\x03 \x01(\x0b\x32\x1e.LocationsAndTimestampsWrapper\"n\n\x1dLocationsAndTimestampsWrapper\x12M\n!recentLocationAndNetworkLocations\x18\x04 \x01(\x0b\x32\".RecentLocationAndNetworkLocations\"\xf3\x01\n!RecentLocationAndNetworkLocations\x12\'\n\x0erecentLocation\x18\x01 \x01(\x0b\x32\x0f.LocationReport\x12&\n\x17recentLocationTimestamp\x18\x02 \x01(\x0b\x32\x05.Time\x12)\n\x10networkLocations\x18\x05 \x03(\x0b\x32\x0f.LocationReport\x12(\n\x19networkLocationTimestamps\x18\x06 \x03(\x0b\x32\x05.Time\x12(\n minLocationsNeededForAggregation\x18\t \x01(\r\"[\n\x11\x41\x63\x63\x65ssInformation\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x11\n\thasAccess\x18\x02 \x01(\x08\x12\x0f\n\x07isOwner\x18\x03 \x01(\x08\x12\x13\n\x0bthisAccount\x18\x04 \x01(\x08\".\n\x0fRequestMetadata\x12\x1b\n\x0cresponseTime\x18\x01 \x01(\x0b\x32\x05.Time\"n\n\x1d\x45ncryptionUnlockRequestExtras\x12\x11\n\toperation\x18\x01 \x01(\x05\x12\'\n\x0esecurityDomain\x18\x02 \x01(\x0b\x32\x0f.SecurityDomain\x12\x11\n\tsessionId\x18\x06 \x01(\t\"/\n\x0eSecurityDomain\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07unknown\x18\x02 \x01(\x05\"A\n\x08Location\x12\x10\n\x08latitude\x18\x01 \x01(\x0f\x12\x11\n\tlongitude\x18\x02 \x01(\x0f\x12\x10\n\x08\x61ltitude\x18\x03 \x01(\x05\"\xb6\x02\n\x18RegisterBleDeviceRequest\x12\x17\n\x0f\x66\x61stPairModelId\x18\x07 \x01(\t\x12\'\n\x0b\x64\x65scription\x18\n \x01(\x0b\x32\x12.DeviceDescription\x12)\n\x0c\x63\x61pabilities\x18\x0b \x01(\x0b\x32\x13.DeviceCapabilities\x12=\n\x19\x65\x32\x65\x65PublicKeyRegistration\x18\x10 \x01(\x0b\x32\x1a.E2EEPublicKeyRegistration\x12\x18\n\x10manufacturerName\x18\x11 \x01(\t\x12\x0f\n\x07ringKey\x18\x15 \x01(\x0c\x12\x13\n\x0brecoveryKey\x18\x16 \x01(\x0c\x12\x1b\n\x13unwantedTrackingKey\x18\x18 \x01(\x0c\x12\x11\n\tmodelName\x18\x19 \x01(\t\"\xaa\x01\n\x19\x45\x32\x45\x45PublicKeyRegistration\x12\x18\n\x10rotationExponent\x18\x01 \x01(\x05\x12\x33\n\x14\x65ncryptedUserSecrets\x18\x03 \x01(\x0b\x32\x15.EncryptedUserSecrets\x12)\n\x0fpublicKeyIdList\x18\x04 \x01(\x0b\x32\x10.PublicKeyIdList\x12\x13\n\x0bpairingDate\x18\x05 \x01(\x05\"\xb9\x01\n\x0fPublicKeyIdList\x12\x39\n\x0fpublicKeyIdInfo\x18\x01 \x03(\x0b\x32 .PublicKeyIdList.PublicKeyIdInfo\x1ak\n\x0fPublicKeyIdInfo\x12\x18\n\ttimestamp\x18\x01 \x01(\x0b\x32\x05.Time\x12\"\n\x0bpublicKeyId\x18\x02 \x01(\x0b\x32\r.TruncatedEID\x12\x1a\n\x12trackableComponent\x18\x03 \x01(\x05\"$\n\x0cTruncatedEID\x12\x14\n\x0ctruncatedEid\x18\x01 \x01(\x0c\"\xe1\x01\n$UploadPrecomputedPublicKeyIdsRequest\x12L\n\ndeviceEids\x18\x01 \x03(\x0b\x32\x38.UploadPrecomputedPublicKeyIdsRequest.DevicePublicKeyIds\x1ak\n\x12\x44\x65vicePublicKeyIds\x12\x1d\n\tcanonicId\x18\x01 \x01(\x0b\x32\n.CanonicId\x12$\n\nclientList\x18\x02 \x01(\x0b\x32\x10.PublicKeyIdList\x12\x10\n\x08pairDate\x18\x03 \x01(\x05\"c\n\x12\x44\x65viceCapabilities\x12\x15\n\risAdvertising\x18\x01 \x01(\x08\x12\x19\n\x11\x63\x61pableComponents\x18\x05 \x01(\x05\x12\x1b\n\x13trackableComponents\x18\x06 \x01(\x05\"\x93\x01\n\x11\x44\x65viceDescription\x12\x17\n\x0fuserDefinedName\x18\x01 \x01(\t\x12#\n\ndeviceType\x18\x02 \x01(\x0e\x32\x0f.SpotDeviceType\x12@\n\x1b\x64\x65viceComponentsInformation\x18\t \x03(\x0b\x32\x1b.DeviceComponentInformation\".\n\x1a\x44\x65viceComponentInformation\x12\x10\n\x08imageUrl\x18\x01 \x01(\t*\xa5\x01\n\nDeviceType\x12\x17\n\x13UNKNOWN_DEVICE_TYPE\x10\x00\x12\x12\n\x0e\x41NDROID_DEVICE\x10\x01\x12\x0f\n\x0bSPOT_DEVICE\x10\x02\x12\x14\n\x10TEST_DEVICE_TYPE\x10\x03\x12\x0f\n\x0b\x41UTO_DEVICE\x10\x04\x12\x13\n\x0f\x46\x41STPAIR_DEVICE\x10\x05\x12\x1d\n\x19SUPERVISED_ANDROID_DEVICE\x10\x07*\xa6\x01\n\x13SpotContributorType\x12\x19\n\x15\x46MDN_DISABLED_DEFAULT\x10\x00\x12!\n\x1d\x46MDN_CONTRIBUTOR_HIGH_TRAFFIC\x10\x03\x12\"\n\x1e\x46MDN_CONTRIBUTOR_ALL_LOCATIONS\x10\x04\x12\x15\n\x11\x46MDN_HIGH_TRAFFIC\x10\x01\x12\x16\n\x12\x46MDN_ALL_LOCATIONS\x10\x02*\x85\x01\n\x0f\x44\x65viceComponent\x12 \n\x1c\x44\x45VICE_COMPONENT_UNSPECIFIED\x10\x00\x12\x1a\n\x16\x44\x45VICE_COMPONENT_RIGHT\x10\x01\x12\x19\n\x15\x44\x45VICE_COMPONENT_LEFT\x10\x02\x12\x19\n\x15\x44\x45VICE_COMPONENT_CASE\x10\x03*`\n\x19IdentifierInformationType\x12\x16\n\x12IDENTIFIER_UNKNOWN\x10\x00\x12\x16\n\x12IDENTIFIER_ANDROID\x10\x01\x12\x13\n\x0fIDENTIFIER_SPOT\x10\x02*\x82\x05\n\x0eSpotDeviceType\x12\x17\n\x13\x44\x45VICE_TYPE_UNKNOWN\x10\x00\x12\x16\n\x12\x44\x45VICE_TYPE_BEACON\x10\x01\x12\x1a\n\x16\x44\x45VICE_TYPE_HEADPHONES\x10\x02\x12\x14\n\x10\x44\x45VICE_TYPE_KEYS\x10\x03\x12\x15\n\x11\x44\x45VICE_TYPE_WATCH\x10\x04\x12\x16\n\x12\x44\x45VICE_TYPE_WALLET\x10\x05\x12\x13\n\x0f\x44\x45VICE_TYPE_BAG\x10\x07\x12\x16\n\x12\x44\x45VICE_TYPE_LAPTOP\x10\x08\x12\x13\n\x0f\x44\x45VICE_TYPE_CAR\x10\t\x12\x1e\n\x1a\x44\x45VICE_TYPE_REMOTE_CONTROL\x10\n\x12\x15\n\x11\x44\x45VICE_TYPE_BADGE\x10\x0b\x12\x14\n\x10\x44\x45VICE_TYPE_BIKE\x10\x0c\x12\x16\n\x12\x44\x45VICE_TYPE_CAMERA\x10\r\x12\x13\n\x0f\x44\x45VICE_TYPE_CAT\x10\x0e\x12\x17\n\x13\x44\x45VICE_TYPE_CHARGER\x10\x0f\x12\x18\n\x14\x44\x45VICE_TYPE_CLOTHING\x10\x10\x12\x13\n\x0f\x44\x45VICE_TYPE_DOG\x10\x11\x12\x18\n\x14\x44\x45VICE_TYPE_NOTEBOOK\x10\x12\x12\x18\n\x14\x44\x45VICE_TYPE_PASSPORT\x10\x13\x12\x15\n\x11\x44\x45VICE_TYPE_PHONE\x10\x14\x12\x17\n\x13\x44\x45VICE_TYPE_SPEAKER\x10\x15\x12\x16\n\x12\x44\x45VICE_TYPE_TABLET\x10\x16\x12\x13\n\x0f\x44\x45VICE_TYPE_TOY\x10\x17\x12\x18\n\x14\x44\x45VICE_TYPE_UMBRELLA\x10\x18\x12\x16\n\x12\x44\x45VICE_TYPE_STYLUS\x10\x19\x12\x17\n\x13\x44\x45VICE_TYPE_EARBUDS\x10\x1a\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ProtoDecoders.DeviceUpdate_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_DEVICETYPE']._serialized_start=4695
  _globals['_DEVICETYPE']._serialized_end=4860
  _globals['_SPOTCONTRIBUTORTYPE']._serialized_start=4863
  _globals['_SPOTCONTRIBUTORTYPE']._serialized_end=5029
  _globals['_DEVICECOMPONENT']._serialized_start=5032
  _globals['_DEVICECOMPONENT']._serialized_end=5165
  _globals['_IDENTIFIERINFORMATIONTYPE']._serialized_start=5167
  _globals['_IDENTIFIERINFORMATIONTYPE']._serialized_end=5263
  _globals['_SPOTDEVICETYPE']._serialized_start=5266
  _globals['_SPOTDEVICETYPE']._serialized_end=5908
  _globals['_GETEIDINFOFORE2EEDEVICESRESPONSE']._serialized_start=64
  _globals['_GETEIDINFOFORE2EEDEVICESRESPONSE']._serialized_end=167
  _globals['_ENCRYPTEDOWNERKEYANDMETADATA']._serialized_start=169
  _globals['_ENCRYPTEDOWNERKEYANDMETADATA']._serialized_end=275
  _globals['_DEVICESLIST']._serialized_start=277
  _globals['_DEVICESLIST']._serialized_end=331
  _globals['_DEVICESLISTREQUEST']._serialized_start=333
  _globals['_DEVICESLISTREQUEST']._serialized_end=415
  _globals['_DEVICESLISTREQUESTPAYLOAD']._serialized_start=417
  _globals['_DEVICESLISTREQUESTPAYLOAD']._serialized_end=483
  _globals['_EXECUTEACTIONREQUEST']._serialized_start=486
  _globals['_EXECUTEACTIONREQUEST']._serialized_end=636
  _globals['_EXECUTEACTIONREQUESTMETADATA']._serialized_start=639
  _globals['_EXECUTEACTIONREQUESTMETADATA']._serialized_end=814
  _globals['_GCMCLOUDMESSAGINGIDPROTOBUF']._serialized_start=816
  _globals['_GCMCLOUDMESSAGINGIDPROTOBUF']._serialized_end=857
  _globals['_EXECUTEACTIONTYPE']._serialized_start=860
  _globals['_EXECUTEACTIONTYPE']._serialized_end=1024
  _globals['_EXECUTEACTIONLOCATETRACKERTYPE']._serialized_start=1026
  _globals['_EXECUTEACTIONLOCATETRACKERTYPE']._serialized_end=1149
  _globals['_EXECUTEACTIONSOUNDTYPE']._serialized_start=1151
  _globals['_EXECUTEACTIONSOUNDTYPE']._serialized_end=1212
  _globals['_EXECUTEACTIONSCOPE']._serialized_start=1214
  _globals['_EXECUTEACTIONSCOPE']._serialized_end=1309
  _globals['_EXECUTEACTIONDEVICEIDENTIFIER']._serialized_start=1311
  _globals['_EXECUTEACTIONDEVICEIDENTIFIER']._serialized_end=1373
  _globals['_DEVICEUPDATE']._serialized_start=1376
  _globals['_DEVICEUPDATE']._serialized_end=1526
  _globals['_DEVICEMETADATA']._serialized_start=1529
  _globals['_DEVICEMETADATA']._serialized_end=1718
  _globals['_IMAGEINFORMATION']._serialized_start=1720
  _globals['_IMAGEINFORMATION']._serialized_end=1756
  _globals['_IDENTITFIERINFORMATION']._serialized_start=1759
  _globals['_IDENTITFIERINFORMATION']._serialized_end=1903
  _globals['_PHONEINFORMATION']._serialized_start=1905
  _globals['_PHONEINFORMATION']._serialized_end=1956
  _globals['_CANONICIDS']._serialized_start=1958
  _globals['_CANONICIDS']._serialized_end=2001
  _globals['_CANONICID']._serialized_start=2003
  _globals['_CANONICID']._serialized_end=2026
  _globals['_DEVICEINFORMATION']._serialized_start=2029
  _globals['_DEVICEINFORMATION']._serialized_end=2195
  _globals['_DEVICETYPEINFORMATION']._serialized_start=2197
  _globals['_DEVICETYPEINFORMATION']._serialized_end=2257
  _globals['_DEVICEREGISTRATION']._serialized_start=2260
  _globals['_DEVICEREGISTRATION']._serialized_end=2468
  _globals['_ENCRYPTEDUSERSECRETS']._serialized_start=2471
  _globals['_ENCRYPTEDUSERSECRETS']._serialized_end=2654
  _globals['_LOCATIONINFORMATION']._serialized_start=2656
  _globals['_LOCATIONINFORMATION']._serialized_end=2726
  _globals['_LOCATIONSANDTIMESTAMPSWRAPPER']._serialized_start=2728
  _globals['_LOCATIONSANDTIMESTAMPSWRAPPER']._serialized_end=2838
  _globals['_RECENTLOCATIONANDNETWORKLOCATIONS']._serialized_start=2841
  _globals['_RECENTLOCATIONANDNETWORKLOCATIONS']._serialized_end=3084
  _globals['_ACCESSINFORMATION']._serialized_start=3086
  _globals['_ACCESSINFORMATION']._serialized_end=3177
  _globals['_REQUESTMETADATA']._serialized_start=3179
  _globals['_REQUESTMETADATA']._serialized_end=3225
  _globals['_ENCRYPTIONUNLOCKREQUESTEXTRAS']._serialized_start=3227
  _globals['_ENCRYPTIONUNLOCKREQUESTEXTRAS']._serialized_end=3337
  _globals['_SECURITYDOMAIN']._serialized_start=3339
  _globals['_SECURITYDOMAIN']._serialized_end=3386
  _globals['_LOCATION']._serialized_start=3388
  _globals['_LOCATION']._serialized_end=3453
  _globals['_REGISTERBLEDEVICEREQUEST']._serialized_start=3456
  _globals['_REGISTERBLEDEVICEREQUEST']._serialized_end=3766
  _globals['_E2EEPUBLICKEYREGISTRATION']._serialized_start=3769
  _globals['_E2EEPUBLICKEYREGISTRATION']._serialized_end=3939
  _globals['_PUBLICKEYIDLIST']._serialized_start=3942
  _globals['_PUBLICKEYIDLIST']._serialized_end=4127
  _globals['_PUBLICKEYIDLIST_PUBLICKEYIDINFO']._serialized_start=4020
  _globals['_PUBLICKEYIDLIST_PUBLICKEYIDINFO']._serialized_end=4127
  _globals['_TRUNCATEDEID']._serialized_start=4129
  _globals['_TRUNCATEDEID']._serialized_end=4165
  _globals['_UPLOADPRECOMPUTEDPUBLICKEYIDSREQUEST']._serialized_start=4168
  _globals['_UPLOADPRECOMPUTEDPUBLICKEYIDSREQUEST']._serialized_end=4393
  _globals['_UPLOADPRECOMPUTEDPUBLICKEYIDSREQUEST_DEVICEPUBLICKEYIDS']._serialized_start=4286
  _globals['_UPLOADPRECOMPUTEDPUBLICKEYIDSREQUEST_DEVICEPUBLICKEYIDS']._serialized_end=4393
  _globals['_DEVICECAPABILITIES']._serialized_start=4395
  _globals['_DEVICECAPABILITIES']._serialized_end=4494
  _globals['_DEVICEDESCRIPTION']._serialized_start=4497
  _globals['_DEVICEDESCRIPTION']._serialized_end=4644
  _globals['_DEVICECOMPONENTINFORMATION']._serialized_start=4646
  _globals['_DEVICECOMPONENTINFORMATION']._serialized_end=4692
# @@protoc_insertion_point(module_scope)
