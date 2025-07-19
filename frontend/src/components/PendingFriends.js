import React, { useState, useEffect } from 'react';
import { 
    Box, 
    VStack, 
    HStack, 
    Text, 
    Avatar, 
    Button, 
    Badge,
    Spinner,
    Alert,
    AlertIcon,
    useToast,
    Heading,
    Divider
} from '@chakra-ui/react';
import { CheckIcon, CloseIcon, TimeIcon } from '@chakra-ui/icons';
import { useAuth } from '../contexts/AuthContext';

const PendingFriends = ({ onCountUpdate }) => {
    const [pendingRequests, setPendingRequests] = useState([]);
    const [loading, setLoading] = useState(true);
    const { token } = useAuth();
    const toast = useToast();

    const fetchPendingRequests = async () => {
        try {
            const response = await fetch('/api/users/pending-friends/', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                setPendingRequests(data);
                if (onCountUpdate) {
                    onCountUpdate(data.length);
                }
            } else {
                throw new Error('Erreur lors du chargement des demandes');
            }
        } catch (error) {
            toast({
                title: 'Erreur',
                description: error.message,
                status: 'error',
                duration: 3000,
                isClosable: true,
            });
        } finally {
            setLoading(false);
        }
    };

    const acceptRequest = async (relationshipId) => {
        try {
            const response = await fetch(`/api/users/accept-friend/${relationshipId}/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                toast({
                    title: 'Succès',
                    description: data.message,
                    status: 'success',
                    duration: 3000,
                    isClosable: true,
                });
                
                // Retirer la demande de la liste
                setPendingRequests(prev => 
                    prev.filter(request => request.id !== relationshipId)
                );
            } else {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Erreur lors de l\'acceptation');
            }
        } catch (error) {
            toast({
                title: 'Erreur',
                description: error.message,
                status: 'error',
                duration: 3000,
                isClosable: true,
            });
        }
    };

    const rejectRequest = async (relationshipId) => {
        try {
            const response = await fetch(`/api/users/reject-friend/${relationshipId}/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                toast({
                    title: 'Succès',
                    description: data.message,
                    status: 'success',
                    duration: 3000,
                    isClosable: true,
                });
                
                // Retirer la demande de la liste
                setPendingRequests(prev => 
                    prev.filter(request => request.id !== relationshipId)
                );
            } else {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Erreur lors du refus');
            }
        } catch (error) {
            toast({
                title: 'Erreur',
                description: error.message,
                status: 'error',
                duration: 3000,
                isClosable: true,
            });
        }
    };

    useEffect(() => {
        fetchPendingRequests();
    }, []);

    if (loading) {
        return (
            <Box p={4} textAlign="center">
                <Spinner size="lg" />
                <Text mt={2}>Chargement des demandes...</Text>
            </Box>
        );
    }

    return (
        <Box p={4}>
            <VStack spacing={4} align="stretch">
                <Heading size="md">
                    Demandes d'amitié ({pendingRequests.length})
                </Heading>

                {pendingRequests.length > 0 ? (
                    <VStack spacing={3} align="stretch">
                        {pendingRequests.map((request) => (
                            <Box
                                key={request.id}
                                p={4}
                                border="1px"
                                borderColor="gray.200"
                                borderRadius="md"
                                bg="white"
                            >
                                <VStack spacing={3} align="stretch">
                                    <HStack spacing={3}>
                                        <Avatar
                                            size="md"
                                            name={request.follower.full_name}
                                            src={request.follower.profile_picture}
                                        />
                                        <VStack align="start" spacing={1} flex={1}>
                                            <Text fontWeight="bold">
                                                {request.follower.full_name}
                                            </Text>
                                            <Text fontSize="sm" color="gray.600">
                                                @{request.follower.username}
                                            </Text>
                                            {request.follower.quartier && (
                                                <Badge colorScheme="blue" size="sm">
                                                    {request.follower.quartier.nom}
                                                </Badge>
                                            )}
                                        </VStack>
                                        <Badge colorScheme="yellow" leftIcon={<TimeIcon />}>
                                            En attente
                                        </Badge>
                                    </HStack>
                                    
                                    {request.follower.bio && (
                                        <Text fontSize="sm" color="gray.600">
                                            {request.follower.bio}
                                        </Text>
                                    )}
                                    
                                    <HStack spacing={2} justify="flex-end">
                                        <Button
                                            size="sm"
                                            colorScheme="red"
                                            variant="outline"
                                            leftIcon={<CloseIcon />}
                                            onClick={() => rejectRequest(request.id)}
                                        >
                                            Refuser
                                        </Button>
                                        <Button
                                            size="sm"
                                            colorScheme="green"
                                            leftIcon={<CheckIcon />}
                                            onClick={() => acceptRequest(request.id)}
                                        >
                                            Accepter
                                        </Button>
                                    </HStack>
                                </VStack>
                            </Box>
                        ))}
                    </VStack>
                ) : (
                    <Alert status="info">
                        <AlertIcon />
                        Aucune demande d'amitié en attente.
                    </Alert>
                )}
            </VStack>
        </Box>
    );
};

export default PendingFriends; 